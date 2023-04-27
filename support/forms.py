from django import forms
from .models import SupportTicket


class SupportTicketForm(forms.ModelForm):

    class Meta:
        model = SupportTicket
        fields = ['name', 'email', 'subject', 'message']


class SupportTicketResponseForm(forms.ModelForm):

    class Meta:
        model = SupportTicket
        fields = ['response', 'name', 'email', 'subject', 'message']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 5})
        }  # optional: customize widget appearance
