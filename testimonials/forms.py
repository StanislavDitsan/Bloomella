from django import forms
from .models import Testimonial


class TestimonialForm(forms.ModelForm):

    class Meta:
        model = Testimonial
        fields = ['name', 'email', 'message']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@example.com'):
            raise forms.ValidationError(
                'Please use an example.com email address')
        return email
