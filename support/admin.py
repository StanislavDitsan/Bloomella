from django.contrib import admin
from .models import SupportTicket
from .forms import SupportTicketResponseForm
from django.utils import timezone


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
        super().save_model(request, obj, form, change)


admin.site.register(SupportTicket, SupportTicketAdmin)