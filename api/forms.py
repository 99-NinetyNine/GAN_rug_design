from django import forms

class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    index = forms.IntegerField(max_value=300,)

class FunImageUploadForm(forms.Form):
    image = forms.ImageField()
    image_2 = forms.ImageField()
