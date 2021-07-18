from django import forms
from django.db import models 
from django.db.models import CharField, TextField
from checkout.models import OrderLineItem



class CustomProductForm(forms.ModelForm):
    class Meta:
        model = OrderLineItem
        fields = ('category', 'complexity', 'variations', 'user_description', 'fast_delivery',)
      
    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)
        labels = {
        'category': 'category',
        'variations': 'Variations',
        'complexity': 'Complexity',
        'fast_delivery': '72 Hour Delivery +15%',
        'user_description': 'Description',
    }

        self.fields['category'].widget.attrs['requiered'] = True
        self.fields['user_description'].widget.attrs['placeholder'] = 'Your product\'s description...'
        self.fields['user_description'].widget.attrs['style'] = 'max-height: 100px'
        
        for field in self.fields:
            self.fields[field].widget.attrs['id'] = field
            self.fields[field].widget.attrs['class'] = 'form-check-input'
            self.fields[field].widget.attrs['onclick'] = 'total()'
            self.fields['user_description'].widget.attrs['class'] = 'form-check-input w-100'
