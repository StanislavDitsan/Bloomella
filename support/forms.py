from django import forms
from .models import SupportTicket


class SupportTicketResponseForm(forms.ModelForm):

    class Meta:
        model = SupportTicket
        fields = ['response']
        widgets = {
            'response': forms.Textarea(attrs={'rows': 5})
        }  # optional: customize widget appearance
