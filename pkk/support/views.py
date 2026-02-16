from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import SupportTicket, TicketMessage
from .forms import CreateTicketForm, TicketMessageForm
from packages.models import Company, Package
from content.models import Order


@login_required
def create_ticket(request):
    """Customer creates a new support ticket"""
    if request.user.user_type != 'user':
        messages.error(request, 'Only customers can create support tickets.')
        return redirect('home')

    # Get companies and orders for dropdowns
    companies = Company.objects.filter(approval_status='approved', is_active=True)
    user_orders = Order.objects.filter(user=request.user)

    if request.method == 'POST':
        form = CreateTicketForm(request.POST)
        company_id = request.POST.get('company')
        order_id = request.POST.get('order')
        package_id = request.POST.get('package')

        if form.is_valid() and company_id:
            ticket = form.save(commit=False)
            ticket.customer = request.user

            try:
                ticket.company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                messages.error(request, 'Please select a valid company.')
                return render(request, 'support/create_ticket.html', {
                    'form': form, 'companies': companies, 'orders': user_orders,
                })

            if order_id:
                try:
                    ticket.order = Order.objects.get(id=order_id, user=request.user)
                except Order.DoesNotExist:
                    pass

            if package_id:
                try:
                    ticket.package = Package.objects.get(id=package_id)
                except Package.DoesNotExist:
                    pass

            ticket.save()

            # Also save the description as the first message
            TicketMessage.objects.create(
                ticket=ticket,
                sender=request.user,
                sender_type='customer',
                message=ticket.description,
            )

            messages.success(request, f'Ticket {ticket.ticket_id} created successfully! The company has 48 hours to respond.')
            return redirect('support:ticket_detail', ticket_id=ticket.ticket_id)
        else:
            if not company_id:
                messages.error(request, 'Please select a company.')
    else:
        form = CreateTicketForm()

    context = {
        'form': form,
        'companies': companies,
        'orders': user_orders,
        'selected_company': request.GET.get('company', request.POST.get('company', '')),
        'selected_order': request.GET.get('order', request.POST.get('order', '')),
        'selected_package': request.GET.get('package', request.POST.get('package', '')),
    }
    return render(request, 'support/create_ticket.html', context)


@login_required
def my_tickets(request):
    """Customer views their support tickets"""
    if request.user.user_type != 'user':
        messages.error(request, 'Only customers can view their tickets.')
        return redirect('home')

    tickets = SupportTicket.objects.filter(customer=request.user)

    # Auto-escalate overdue tickets
    for ticket in tickets:
        if ticket.is_overdue and ticket.status == 'pending_company':
            ticket.escalate()

    # Refresh after possible escalation
    tickets = SupportTicket.objects.filter(customer=request.user)

    status_filter = request.GET.get('status', '')
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    context = {
        'tickets': tickets,
        'status_filter': status_filter,
    }
    return render(request, 'support/my_tickets.html', context)


@login_required
def ticket_detail(request, ticket_id):
    """View ticket details and conversation"""
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)

    # Access control: customer, company owner, or admin
    user = request.user
    is_customer = (user == ticket.customer)
    is_company = (user.user_type == 'company' and hasattr(ticket.company, 'owner') and ticket.company.owner == user)
    is_admin = user.is_staff

    if not (is_customer or is_company or is_admin):
        messages.error(request, 'You do not have permission to view this ticket.')
        return redirect('home')

    # Auto-escalate if overdue
    if ticket.is_overdue and ticket.status == 'pending_company':
        ticket.escalate()

    # Handle reply
    if request.method == 'POST':
        reply_form = TicketMessageForm(request.POST, request.FILES)
        if reply_form.is_valid():
            msg = reply_form.save(commit=False)
            msg.ticket = ticket
            msg.sender = user

            if is_admin:
                msg.sender_type = 'admin'
            elif is_company:
                msg.sender_type = 'company'
                # Mark first response time
                if not ticket.first_response_at:
                    ticket.first_response_at = timezone.now()
                # Move to in_progress if company responds
                if ticket.status == 'pending_company':
                    ticket.status = 'in_progress'
                    ticket.save()
            else:
                msg.sender_type = 'customer'

            msg.save()
            ticket.updated_at = timezone.now()
            ticket.save()
            messages.success(request, 'Reply sent successfully.')
            return redirect('support:ticket_detail', ticket_id=ticket.ticket_id)
    else:
        reply_form = TicketMessageForm()

    ticket_messages = ticket.messages.all()

    context = {
        'ticket': ticket,
        'messages_list': ticket_messages,
        'reply_form': reply_form,
        'is_customer': is_customer,
        'is_company': is_company,
        'is_admin': is_admin,
    }
    return render(request, 'support/ticket_detail.html', context)


@login_required
def company_tickets(request):
    """Company views tickets assigned to them"""
    if request.user.user_type != 'company':
        messages.error(request, 'Only companies can access this page.')
        return redirect('home')

    company = Company.objects.filter(owner=request.user).first()
    if not company:
        messages.error(request, 'No company found for your account.')
        return redirect('home')

    tickets = SupportTicket.objects.filter(company=company)

    # Auto-escalate overdue tickets
    for ticket in tickets:
        if ticket.is_overdue and ticket.status == 'pending_company':
            ticket.escalate()

    tickets = SupportTicket.objects.filter(company=company)

    status_filter = request.GET.get('status', '')
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    context = {
        'tickets': tickets,
        'company': company,
        'status_filter': status_filter,
    }
    return render(request, 'support/company_tickets.html', context)


@login_required
def resolve_ticket(request, ticket_id):
    """Company or admin resolves a ticket"""
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
    user = request.user

    is_company = (user.user_type == 'company' and hasattr(ticket.company, 'owner') and ticket.company.owner == user)
    is_admin = user.is_staff

    if not (is_company or is_admin):
        messages.error(request, 'No permission to resolve this ticket.')
        return redirect('home')

    if request.method == 'POST':
        ticket.resolve(resolved_by='admin' if is_admin else 'company')
        messages.success(request, f'Ticket {ticket.ticket_id} has been resolved.')

        if is_admin:
            return redirect('support:admin_tickets')
        return redirect('support:company_tickets')

    return redirect('support:ticket_detail', ticket_id=ticket.ticket_id)


@login_required
def escalate_ticket(request, ticket_id):
    """Customer manually escalates a ticket (available after deadline)"""
    ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)

    if request.user != ticket.customer:
        messages.error(request, 'Only the ticket creator can escalate.')
        return redirect('home')

    if ticket.status in ['resolved', 'closed']:
        messages.info(request, 'This ticket is already resolved.')
        return redirect('support:ticket_detail', ticket_id=ticket.ticket_id)

    if ticket.is_overdue or ticket.status == 'pending_company':
        ticket.escalate()
        messages.success(request, f'Ticket {ticket.ticket_id} has been escalated to an admin.')
    else:
        messages.info(request, 'This ticket cannot be escalated yet. The company still has time to respond.')

    return redirect('support:ticket_detail', ticket_id=ticket.ticket_id)


@login_required
def admin_tickets(request):
    """Admin views all escalated tickets"""
    if not request.user.is_staff:
        messages.error(request, 'Admin access required.')
        return redirect('home')

    tickets = SupportTicket.objects.filter(
        Q(status='escalated') | Q(escalated_to_admin=True)
    )

    show_all = request.GET.get('all', '')
    if show_all:
        tickets = SupportTicket.objects.all()

    status_filter = request.GET.get('status', '')
    if status_filter:
        tickets = tickets.filter(status=status_filter)

    context = {
        'tickets': tickets,
        'show_all': show_all,
        'status_filter': status_filter,
    }
    return render(request, 'support/admin_tickets.html', context)
