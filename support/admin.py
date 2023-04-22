from django.contrib import admin
from .models import SupportTicket
from .forms import SupportTicketResponseForm
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings


class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'updated_at',
                    'response')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('name', 'email', 'subject', 'message', 'response')

    def get_form(self, request, obj=None, **kwargs):
        if obj:
            return SupportTicketResponseForm
        else:
            return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        if obj.response and change:
            # if the admin has added a response, update the updated_at field
            obj.updated_at = timezone.now()

            # send email notification to user
            subject = f"Response to your support ticket: {obj.subject}"
            message = f"Dear {obj.name},\n\nWe have responded to your support ticket regarding '{obj.subject}':\n\n{obj.response}\n\nThank you for using our support service.\n\nBest regards,\nThe Support Team"
            from_email = settings.EMAIL_HOST_USER
            recipient_list = [obj.email]
            send_mail(subject, message, from_email, recipient_list)

        super().save_model(request, obj, form, change)


admin.site.register(SupportTicket, SupportTicketAdmin)