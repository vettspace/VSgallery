from django import forms

from .models import PhotoSession


class PhotoSessionForm(forms.ModelForm):
    class Meta:
        model = PhotoSession
        fields = ['title', 'client_name']
        labels = {
            'title': 'Название',
            'client_name': 'Имя клиента',
        }

class PhotoForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(),
        required=True,
        label='Изображения'
    )