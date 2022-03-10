from django import forms
from django.forms import HiddenInput, ModelForm

CATEGORIES_CHOICES =(
    ("Electronic", "Electronic"),
    ("Furniture", "Furniture"),
    ("Books", "Books"),
    ("Clothes", "Clothes"),
    ("Videogames", "Videogames"),
    )
    
class createlisting(forms.Form):
    Product = forms.CharField(label='Products name', max_length=64, widget=forms.TextInput(attrs={'class': "prdct"}))
    Description = forms.CharField(label='Add a description to the auction', max_length=800, widget=forms.Textarea(attrs={'class': "descq"}))
    Price = forms.DecimalField(decimal_places= 2, max_digits=6, widget=forms.NumberInput(attrs={'class': "prdct"}))
    Image = forms.URLField(label='If you want to put an image, paste here the url', required=False, widget=forms.TextInput(attrs={'class': "prdct"}))
    Category = forms.ChoiceField(label='Category', choices= CATEGORIES_CHOICES)
    
class newoffer(forms.Form):
    offer = forms.DecimalField(label="",decimal_places=2, max_digits=10, widget=forms.TextInput(attrs={'class': "form-control"}))

class newcomment(forms.Form):
    comment = forms.CharField(label="", max_length=280, widget=forms.Textarea(attrs={'class': "comm"}))
