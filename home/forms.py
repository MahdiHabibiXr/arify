from django import forms
from django.forms import TextInput, FileInput
from .models import Nerf, Video, ApiKey


class NerfCreateForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ('title', 'video')
        labels = {'title': 'Enter the title', 'video': 'Upload your video'}
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'style': 'max-width: 300px;',
                'placeholder': 'Name'
            }),
            'video': FileInput(attrs={
                'accept': 'video/*'
            }),
        }


class NerfEditForm(forms.ModelForm):
    class Meta:
        model = Nerf
        fields = ('slug', )


class ApiKeyCreatForm(forms.ModelForm):
    class Meta:
        model = ApiKey
        fields = ('key', 'remaining', )
