from django import forms
from .models import E
class EForm(forms.ModelForm):
    class Meta:
        model = E
        fields = ('e_date', 'detail_public', 'detail_private', 'notes', 'attendees')
