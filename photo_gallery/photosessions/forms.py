from django import forms

from .models import PhotoSession


class PhotoSessionForm(forms.ModelForm):
    class Meta:
        model = PhotoSession
        fields = ['title']
        labels = {
            'title': 'Название',
        }

class PhotoForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(),
        required=True,
        label='Изображения'
    )
