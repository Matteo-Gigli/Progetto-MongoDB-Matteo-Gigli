from django.shortcuts import render, redirect
from .forms import Registration
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from app.models import Customer
import random
from django.contrib import messages

def registration(request):
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
            )
            new_customer = Customer(
                user=user,
                btc_wallet=random.randrange(1, 11),
            )
            new_customer.dollar_wallet = new_customer.btc_wallet * float(40000)
            new_customer.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Welcome to MGExchange {new_customer.user}. You recived {new_customer.btc_wallet} bitcoin for the Registration.')
            return redirect('/homepage/')
    else:
        form = Registration()
        context = {'form': form}
        return render(request, 'registration_form.html', context)


