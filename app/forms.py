from django import forms
from .models import OrderToSell, OrderToBuy

class PublishOrderToBuy(forms.ModelForm):
    class Meta:
        model = OrderToBuy
        fields = ['price', 'quantity']


class PublishOrderToSell(forms.ModelForm):
    class Meta:
        model = OrderToSell
        fields = ['price', 'quantity']