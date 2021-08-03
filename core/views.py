from django.shortcuts import render, get_object_or_404, redirect, reverse
from app.models import Customer, OrderToSell, OrderToBuy

def homepage(request):
    customer = Customer.objects.get(user=request.user)
    order_sell = OrderToSell.objects.filter().order_by('-publish_on')
    order_buy = OrderToBuy.objects.filter().order_by('-publish_on')
    context = {'customer': customer, 'order_sell': order_sell, 'order_buy': order_buy}
    return render(request, 'homepage.html', context)
