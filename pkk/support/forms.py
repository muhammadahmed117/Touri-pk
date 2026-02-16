from django import forms
from .models import SupportTicket, TicketMessage


class CreateTicketForm(forms.ModelForm):
    """Form for customers to create support tickets"""

    class Meta:
        model = SupportTicket
        fields = ['subject', 'description', 'issue_type', 'priority']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief summary of your issue',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe your issue in detail...',
            }),
            'issue_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'priority': forms.Select(attrs={
                'class': 'form-control',
            }),
        }


class TicketMessageForm(forms.ModelForm):
    """Form to add a message/reply to a ticket"""

    class Meta:
        model = TicketMessage
        fields = ['message', 'attachment']
        widgets = {
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Type your reply...',
            }),
            'attachment': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
