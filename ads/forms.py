from django import forms
from .models import Ad
from ckeditor.widgets import CKEditorWidget

class AdForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Ad
        fields = ['title', 'text', 'category']