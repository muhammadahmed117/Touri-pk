from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
import random
import string


class SupportTicket(models.Model):
    """Customer support ticket model"""

    ISSUE_TYPE_CHOICES = [
        ('delivery', 'Delivery Issue'),
        ('quality', 'Product Quality'),
        ('package_issue', 'Package/Tour Issue'),
        ('billing', 'Billing / Payment'),
        ('booking', 'Booking Problem'),
        ('refund', 'Refund Request'),
        ('other', 'Other'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending_company', 'Waiting for Company'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('escalated', 'Escalated to Admin'),
        ('closed', 'Closed'),
    ]

    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='support_tickets'
    )
    company = models.ForeignKey(
        'packages.Company', on_delete=models.CASCADE, related_name='support_tickets'
    )

    # Optional links to related objects
    order = models.ForeignKey(
        'content.Order', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets'
    )
    package = models.ForeignKey(
        'packages.Package', on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets'
    )

    subject = models.CharField(max_length=200)
    description = models.TextField()
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES, default='other')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending_company')

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_response_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    escalated_at = models.DateTimeField(null=True, blank=True)

    # Escalation
    escalation_deadline = models.DateTimeField(null=True, blank=True)
    escalated_to_admin = models.BooleanField(default=False)
    admin_notes = models.TextField(blank=True)

    class Meta:
        ordering = ['created_at']  # FIFO queue: oldest first

    def __str__(self):
        return f"{self.ticket_id} - {self.subject}"

    def save(self, *args, **kwargs):
        if not self.ticket_id:
            self.ticket_id = 'TKT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not self.escalation_deadline:
            self.escalation_deadline = (self.created_at or timezone.now()) + timedelta(hours=48)
        super().save(*args, **kwargs)

    @property
    def is_overdue(self):
        """Check if company response deadline has passed"""
        if self.status in ['resolved', 'closed']:
            return False
        return timezone.now() > self.escalation_deadline

    @property
    def time_remaining(self):
        """Remaining time before auto-escalation"""
        if self.status in ['resolved', 'closed', 'escalated']:
            return timedelta(0)
        remaining = self.escalation_deadline - timezone.now()
        return remaining if remaining.total_seconds() > 0 else timedelta(0)

    @property
    def time_remaining_hours(self):
        remaining = self.time_remaining
        total_seconds = int(remaining.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours}h {minutes}m"

    def escalate(self):
        """Escalate ticket to admin"""
        self.status = 'escalated'
        self.escalated_to_admin = True
        self.escalated_at = timezone.now()
        self.save()

    def resolve(self, resolved_by='company'):
        """Mark ticket as resolved"""
        self.status = 'resolved'
        self.resolved_at = timezone.now()
        self.save()


class TicketMessage(models.Model):
    """Messages within a support ticket (conversation thread)"""

    SENDER_TYPE_CHOICES = [
        ('customer', 'Customer'),
        ('company', 'Company'),
        ('admin', 'Admin'),
    ]

    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    sender_type = models.CharField(max_length=10, choices=SENDER_TYPE_CHOICES)
    message = models.TextField()
    attachment = models.FileField(upload_to='support/attachments/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender_type}: {self.message[:50]}"
