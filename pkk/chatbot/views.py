import json
import requests
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatSession, ChatMessage
from .config import DEEPSEEK_API_KEY, DEEPSEEK_API_URL
from .prompt_builder import (
    build_context_aware_messages,
    detect_irrelevant_keywords,
    get_quick_response_for_common_questions
)
import logging

logger = logging.getLogger(__name__)

def get_deepseek_response(message, session=None):
    """
    Get AI response with website-specific training and irrelevant question filtering.

    Args:
        message: User's message
        session: ChatSession object for conversation context

    Returns:
        AI-generated response or quick response
    """

    # Check for quick responses to common questions (no API call needed)
    quick_response = get_quick_response_for_common_questions(message)
    if quick_response:
        logger.info(f"Returning quick response for common question")
        return quick_response

    # Pre-filter obviously irrelevant questions
    if detect_irrelevant_keywords(message):
        logger.info(f"Detected irrelevant question, returning boundary response")
        return "I'm specifically designed to help with TouriPK website and Pakistan tourism. I can assist you with:\n\n🏔️ Exploring our 12 featured destinations\n💰 Estimating trip costs\n📦 Finding tour packages\n🌤️ Checking weather forecasts\n🛍️ Shopping local products\n\nWhat would you like to know about planning your trip to Pakistan?"

    # Get conversation history if session provided
    chat_history = []
    if session:
        recent_messages = session.messages.order_by('-created_at')[:5]
        chat_history = [
            {'message': msg.message, 'response': msg.response}
            for msg in reversed(list(recent_messages))
        ]

    # Build context-aware messages with comprehensive training
    messages = build_context_aware_messages(message, chat_history)

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "deepseek-chat",
        "messages": messages,
        "max_tokens": 600,
        "temperature": 0.7,
        "top_p": 0.95
    }
    
    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            ai_response = response.json()["choices"][0]["message"]["content"]
            logger.info(f"AI response generated successfully")
            return ai_response
        else:
            logger.error(f"API Error: {response.status_code}, {response.text}")
            return "Sorry, I'm having trouble connecting right now. Please try again later. In the meantime, you can:\n• Browse destinations at /content/destinations/\n• Check packages at /packages/\n• Use cost calculator at /content/calculator/"
    except requests.Timeout:
        logger.error("API request timed out")
        return "Sorry, the request took too long. Please try again, or browse our website:\n• Destinations: /content/destinations/\n• Packages: /packages/\n• Calculator: /content/calculator/"
    except Exception as e:
        logger.error(f"Error in API call: {str(e)}")
        return "Sorry, I'm experiencing technical difficulties. You can still explore:\n• Destinations: /content/destinations/\n• Packages: /packages/\n• Calculator: /content/calculator/"



@login_required
def chatbot_view(request):
    """
    Redirect to home page with chatbot widget visible.
    The chatbot is now a floating widget on all pages via base template.
    """
    from django.shortcuts import redirect
    return redirect('home')


@login_required
@csrf_exempt
def send_message(request):
    logger.debug(f"send_message called with method: {request.method}")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message = data.get('message', '').strip()
            session_id = data.get('session_id')
            logger.debug(f"Received message: '{message}', session_id: {session_id}")
            
            if not message:
                logger.warning("Empty message received")
                return JsonResponse({'error': 'Message cannot be empty'}, status=400)
            
            if session_id:
                session = get_object_or_404(ChatSession, id=session_id, user=request.user)
                logger.debug(f"Using existing session: {session.id}")
            else:
                session = ChatSession.objects.create(
                    user=request.user,
                    title=message[:50] + "..." if len(message) > 50 else message
                )
                logger.debug(f"Created new session: {session.id}")
            
            # Pass session for context-aware responses
            ai_response = get_deepseek_response(message, session=session)
            logger.debug(f"AI response generated")

            chat_message = ChatMessage.objects.create(
                session=session,
                message=message,
                response=ai_response
            )
            logger.debug(f"Saved message with ID: {chat_message.id}")
            
            response_data = {
                'response': ai_response,
                'session_id': session.id,
                'message_id': chat_message.id
            }
            
            return JsonResponse(response_data)
        except json.JSONDecodeError:
            logger.error("Invalid JSON in request body")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            logger.error(f"Error in send_message: {str(e)}", exc_info=True)
            return JsonResponse({'error': f'Server error: {str(e)}'}, status=500)
    
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def get_chat_history(request, session_id):
    print(f"DEBUG: get_chat_history called for session_id: {session_id}")
    try:
        session = get_object_or_404(ChatSession, id=session_id, user=request.user)
        messages = session.messages.all().order_by('created_at')
        print(f"DEBUG: Found {messages.count()} messages for session {session_id}")
        
        data = []
        for msg in messages:
            msg_data = {
                'message': msg.message,
                'response': msg.response,
                'created_at': msg.created_at.strftime('%H:%M')
            }
            data.append(msg_data)
            print(f"DEBUG: Message - User: '{msg.message}', Bot: '{msg.response}'")
        
        response_data = {'messages': data, 'title': session.title}
        print(f"DEBUG: Returning chat history: {len(data)} messages")
        return JsonResponse(response_data)
    except Exception as e:
        print(f"DEBUG: Error in get_chat_history: {str(e)}")
        return JsonResponse({'error': f'Error loading history: {str(e)}'}, status=500)
    