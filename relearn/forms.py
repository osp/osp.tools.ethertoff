from django import forms
from django.utils.translation import ugettext_lazy as _


class ContactForm(forms.Form):
    name         = forms.CharField(max_length=50, label=_("First Name"))
    email        = forms.EmailField(label=_("E-Mail"))
    subject      = forms.CharField(max_length=100, label=_("Subject"))
    message      = forms.CharField(widget=forms.Textarea(), label=_("Message"))
