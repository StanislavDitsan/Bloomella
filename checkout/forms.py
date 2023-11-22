from django import forms
from .models import Order


class OrderForm(forms.ModelForm):

    delivery_day = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        required=False,
        help_text='Select a delivery day'
    )

    recipient_phone_number = forms.CharField(
        max_length=20,
        required=True,
        help_text='Recipient phone number'
    )

    card_note = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.Textarea(attrs={'rows': 2}),
        help_text='Note for the card (max 100 characters)'
    )

    class Meta:
        model = Order
        fields = (
            'full_name',
            'email',
            'phone_number',
            'street_address1',
            'street_address2',
            'town_or_city',
            'postcode',
            'country',
            'county',
            'delivery_day',
            'recipient_phone_number',
            'card_note',
)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'delivery_day': 'Select a delivery day',
            'recipient_phone_number': 'Recipient phone number',
            'card_note': 'Note for the card (max 100 characters)',
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County, State or Locality',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
