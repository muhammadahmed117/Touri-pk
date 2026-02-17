"""Security utilities for data protection and validation"""
import os
import mimetypes
from django.core.exceptions import ValidationError
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


def validate_file_upload(uploaded_file, allowed_extensions=None, max_size_mb=5):
    """
    Validate uploaded files for security
    
    Args:
        uploaded_file: UploadedFile object
        allowed_extensions: List of allowed extensions (default: images)
        max_size_mb: Maximum file size in MB
    
    Raises:
        ValidationError: If file is invalid
    """
    if not uploaded_file:
        return
    
    # Default to image extensions
    if allowed_extensions is None:
        allowed_extensions = getattr(settings, 'ALLOWED_IMAGE_EXTENSIONS', 
                                     ['jpg', 'jpeg', 'png', 'gif', 'webp'])
    
    # Check file size
    max_size = max_size_mb * 1024 * 1024
    if uploaded_file.size > max_size:
        raise ValidationError(f'File size exceeds {max_size_mb}MB limit')
    
    # Get file extension
    file_name = uploaded_file.name.lower()
    file_ext = os.path.splitext(file_name)[1][1:]  # Remove the dot
    
    # Validate extension
    if file_ext not in allowed_extensions:
        raise ValidationError(
            f'File type .{file_ext} not allowed. Allowed types: {", ".join(allowed_extensions)}'
        )
    
    # Validate MIME type
    mime_type, _ = mimetypes.guess_type(file_name)
    if mime_type:
        # For images, ensure it's actually an image MIME type
        if 'image' in allowed_extensions[0] or file_ext in ['jpg', 'jpeg', 'png', 'gif', 'webp']:
            if not mime_type.startswith('image/'):
                raise ValidationError('File content does not match image type')
    
    # Check for dangerous file names
    dangerous_patterns = ['..', '/', '\\', '<', '>', ':', '"', '|', '?', '*']
    for pattern in dangerous_patterns:
        if pattern in file_name:
            raise ValidationError('File name contains invalid characters')
    
    logger.info(f"File validated: {file_name} ({uploaded_file.size} bytes)")
    return True


def sanitize_user_input(text, max_length=1000):
    """
    Sanitize user text input
    
    Args:
        text: User input string
        max_length: Maximum allowed length
    
    Returns:
        Sanitized string
    """
    if not text:
        return ''
    
    # Convert to string and strip
    text = str(text).strip()
    
    # Limit length
    if len(text) > max_length:
        text = text[:max_length]
    
    # Remove null bytes
    text = text.replace('\x00', '')
    
    # Remove excessive whitespace
    text = ' '.join(text.split())
    
    return text


def mask_sensitive_data(data, fields_to_mask=None):
    """
    Mask sensitive data for logging
    
    Args:
        data: Dictionary or string
        fields_to_mask: List of field names to mask
    
    Returns:
        Masked data safe for logging
    """
    if fields_to_mask is None:
        fields_to_mask = ['password', 'password1', 'password2', 'token', 'secret', 
                         'api_key', 'stripe', 'card', 'cvv', 'ssn', 'cnic']
    
    if isinstance(data, dict):
        masked = {}
        for key, value in data.items():
            # Check if field name contains sensitive keywords
            if any(sensitive in key.lower() for sensitive in fields_to_mask):
                masked[key] = '***MASKED***'
            elif isinstance(value, dict):
                masked[key] = mask_sensitive_data(value, fields_to_mask)
            else:
                masked[key] = value
        return masked
    
    elif isinstance(data, str):
        # For strings, just check if it looks like sensitive data
        if len(data) > 50:
            return data[:20] + '...' + data[-10:]
        return data
    
    return data


def check_user_owns_resource(user, resource, owner_field='user'):
    """
    Check if user owns a resource
    
    Args:
        user: User object
        resource: Model instance
        owner_field: Field name that contains the owner
    
    Returns:
        bool: True if user owns resource
    """
    try:
        owner = getattr(resource, owner_field)
        return owner == user
    except AttributeError:
        logger.error(f"Resource {type(resource)} does not have field {owner_field}")
        return False


def log_security_event(event_type, user, details, level='info'):
    """
    Log security-related events
    
    Args:
        event_type: Type of event (login, logout, access_denied, etc.)
        user: User object or username
        details: Event details (will be masked)
        level: Log level (info, warning, error)
    """
    username = user.username if hasattr(user, 'username') else str(user)
    masked_details = mask_sensitive_data(details)
    
    log_message = f"SECURITY [{event_type}] User: {username} - {masked_details}"
    
    if level == 'warning':
        logger.warning(log_message)
    elif level == 'error':
        logger.error(log_message)
    else:
        logger.info(log_message)
