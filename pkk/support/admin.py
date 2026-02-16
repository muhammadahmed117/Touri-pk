from django.contrib import admin
from .models import SupportTicket, TicketMessage


class TicketMessageInline(admin.TabularInline):
    model = TicketMessage
    extra = 0
    readonly_fields = ['sender', 'sender_type', 'created_at']


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'subject', 'customer', 'company', 'issue_type', 'status', 'priority', 'created_at', 'is_overdue']
    list_filter = ['status', 'priority', 'issue_type', 'escalated_to_admin']
    search_fields = ['ticket_id', 'subject', 'customer__username', 'company__name']
    readonly_fields = ['ticket_id', 'created_at', 'updated_at', 'escalation_deadline']
    ordering = ('created_at',)  # FIFO queue: oldest first
    inlines = [TicketMessageInline]

    def is_overdue(self, obj):
        return obj.is_overdue
    is_overdue.boolean = True


@admin.register(TicketMessage)
class TicketMessageAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'sender', 'sender_type', 'created_at']
    list_filter = ['sender_type']
