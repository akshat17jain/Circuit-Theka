from django import forms
from .models import *

class ImageForm(forms.Form):
    image = forms.ImageField(label = 'Choose an image below.')
