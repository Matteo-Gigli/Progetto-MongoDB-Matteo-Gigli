from django.contrib import admin
from .models import Customer, OrderToBuy, OrderToSell

admin.site.register([Customer, OrderToBuy, OrderToSell])
# Register your models here.
