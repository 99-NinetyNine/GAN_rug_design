from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

class FunImageUploadForm(forms.Form):
    image = forms.ImageField()
    image_2 = forms.ImageField()
