from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    btc_wallet = models.FloatField(default=0)
    dollar_wallet = models.FloatField(default=0)
    profit = models.FloatField(default=0)


class OrderToSell(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    publish_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class OrderToBuy(models.Model):
    price = models.FloatField(default=0)
    quantity = models.FloatField(default=0)
    publish_on = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)