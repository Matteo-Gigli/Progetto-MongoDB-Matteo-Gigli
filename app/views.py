from django.shortcuts import render, redirect
from .models import Customer, OrderToBuy, OrderToSell
from .forms import PublishOrderToBuy, PublishOrderToSell
from django.contrib import messages
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["Progetto_MongoDB_di_Matteo_Gigli"]

def publish_order_to_buy(request):
    customer = Customer.objects.get(user=request.user)
    order_sell = OrderToSell.objects.filter().order_by('-publish_on')
    if request.method == 'POST':
        form = PublishOrderToBuy(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = customer
            price = form.price
            quantity = form.quantity
            if price < 0.0:
                messages.error(request, 'Cannot put a price lower than 0')
                return redirect('/homepage/')
            if quantity < 0.0:
                messages.error(request, 'Cannot put a quantity lower than 0')
                return redirect('/homepage/')

            if customer.dollar_wallet >= price and customer.dollar_wallet > 0:
                for order in order_sell:
                    if price == order.price and quantity == order.quantity:
                        customer.dollar_wallet = customer.dollar_wallet - float(price)
                        customer.btc_wallet = customer.btc_wallet + float(quantity)
                        user = order.customer
                        user.btc_wallet = user.btc_wallet
                        user.dollar_wallet = user.dollar_wallet + float(price)
                        customer.profit -= order.price
                        user.profit += order.price
                        customer.save()
                        user.save()
                        messages.success(
                            request, f'You have a match. Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $'
                        )
                        my_coll = mydb['Customer buy an equal order to sell']
                        order_to_buy_transaction = {
                            'User sell his btc': order.customer.user.username,
                            'Selling User Id': order.customer.user.pk,
                            'Selling User $ amount before transaction': order.customer.dollar_wallet - price,
                            'Selling User $ amount after transaction': order.customer.dollar_wallet,
                            'Selling User btc Balance before transaction': order.customer.btc_wallet + quantity,
                            'Selling User btc Balance after transaction': order.customer.btc_wallet,
                            'Order price': price,
                            'Order quantity': quantity,
                            'Buying User': customer.user.username,
                            'Buying user id': customer.user.pk,
                            'Buying User btc Balance before transaction': customer.btc_wallet - quantity,
                            'Buying User btc Balance after transaction': customer.btc_wallet,
                            'Buying User $ before transaction': customer.dollar_wallet + price,
                            'Buying User $ after transaction': customer.dollar_wallet,
                            }
                        x = my_coll.insert_one(order_to_buy_transaction)
                        order.delete()
                        return redirect('/homepage/')


                    if price != order.price and quantity == order.quantity:
                        average_max = int(order.price + order.price /100 * 0.3)
                        average_min = int(order.price)
                        average_range = range(average_min, average_max)
                        if price in average_range and customer.dollar_wallet >= average_max:
                            customer.dollar_wallet = customer.dollar_wallet - float(price)
                            customer.btc_wallet = customer.btc_wallet + float(quantity)
                            user = order.customer
                            user.btc_wallet = user.btc_wallet
                            user.dollar_wallet = user.dollar_wallet + float(price)
                            customer.profit -= price
                            user.profit += price
                            customer.save()
                            user.save()
                            messages.success(
                                request,
                                f'You have a match. Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $'
                                f'is a price different'

                            )
                            my_coll = mydb['Customer buy an average order to sell']
                            order_to_buy_average_price_transaction = {
                                'User sell his btc': order.customer.user.username,
                                'Selling User Id': order.customer.user.pk,
                                'Selling User $ amount before transaction': order.customer.dollar_wallet - price,
                                'Selling User $ amount after transaction': order.customer.dollar_wallet,
                                'Selling User btc Balance before transaction': order.customer.btc_wallet + quantity,
                                'Selling User btc Balance after transaction': order.customer.btc_wallet,
                                'Order price': price,
                                'Order quantity': quantity,
                                'Buying User': customer.user.username,
                                'Buying user id': customer.user.pk,
                                'Buying User btc Balance before transaction': customer.btc_wallet - quantity,
                                'Buying User btc Balance after transaction': customer.btc_wallet,
                                'Buying User $ before transaction': customer.dollar_wallet + price,
                                'Buying User $ after transaction': customer.dollar_wallet,
                            }
                            x = my_coll.insert_one(order_to_buy_average_price_transaction)
                            order.delete()
                            return redirect('/homepage/')

                        else:
                            if price not in average_range:
                                customer.dollar_wallet = customer.dollar_wallet
                                customer.save()
                                form.save()
                                messages.success(request, ' Your order is in the waiting list')
                                return redirect('/homepage/')


                    if quantity != order.quantity and price == order.price:
                        if order.quantity >= quantity:
                            customer.dollar_wallet = customer.dollar_wallet - float(price)
                            customer.btc_wallet = customer.btc_wallet + float(order.quantity)
                            user = order.customer
                            user.btc_wallet = user.btc_wallet
                            user.dollar_wallet = user.dollar_wallet + float(price)
                            customer.profit -= price
                            user.profit += price
                            customer.save()
                            user.save()
                            messages.success(
                                request,
                                f'You have a match. Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $'                   
                                f'You bought {order.quantity} btc and you spent {order.price}'
                            )
                            my_coll = mydb['Customer buy different quantity order to sell']
                            order_to_buy_different_quantity_transaction = {
                                'User sell his btc': order.customer.user.username,
                                'Selling User Id': order.customer.user.pk,
                                'Selling User $ amount before transaction': order.customer.dollar_wallet - price,
                                'Selling User $ amount after transaction': order.customer.dollar_wallet,
                                'Selling User btc Balance before transaction': order.customer.btc_wallet + quantity,
                                'Selling User btc Balance after transaction': order.customer.btc_wallet,
                                'Order price': price,
                                'Order quantity': quantity,
                                'Buying User': customer.user.username,
                                'Buying user id': customer.user.pk,
                                'Buying User btc Balance before transaction': customer.btc_wallet - quantity,
                                'Buying User btc Balance after transaction': customer.btc_wallet,
                                'Buying User $ before transaction': customer.dollar_wallet + price,
                                'Buying User $ after transaction': customer.dollar_wallet,
                            }
                            x = my_coll.insert_one(order_to_buy_different_quantity_transaction)
                            order.delete()
                            return redirect('/homepage/')

                        else:
                            if order.quantity < quantity:
                                customer.dollar_wallet = customer.dollar_wallet
                                customer.save()
                                form.save()
                                messages.success(request, ' Your order is in the waiting list')
                                return redirect('/homepage/')


                else:
                    order = OrderToBuy(customer=customer, price=price, quantity=quantity)
                    customer.dollar_wallet = customer.dollar_wallet - float(price)
                    customer.btc_wallet = customer.btc_wallet
                    order.save()
                    customer.save()
                    messages.success(request, 'Your order is in the waiting list')
                    return redirect('/homepage/')

            else:
                messages.error(request, 'No necessary funds to do this transaction ')
                return redirect('/homepage/')

    else:
        form = PublishOrderToBuy()
        context = {'form': form}
        return render(request, 'publish_order_to_buy.html', context)


def publish_order_to_sell(request):
    customer = Customer.objects.get(user=request.user)
    order_buy = OrderToBuy.objects.filter().order_by('-publish_on')
    if request.method == 'POST':
        form = PublishOrderToSell(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user = customer
            price = form.price
            quantity = form.quantity
            if quantity < 0.0:
                messages.error(request, 'Cannot put a quantity lower than 0')
                return redirect('/homepage/')
            if price < 0.0:
                messages.error(request, 'Cannot put a quantity lower than 0')
                return redirect('/homepage/')

            if customer.btc_wallet >= quantity and customer.btc_wallet > 0.0:
                for order in order_buy:
                    if quantity == order.quantity and price == order.price:
                        customer.btc_wallet = customer.btc_wallet - float(quantity)
                        customer.dollar_wallet = customer.dollar_wallet + float(price)
                        user = order.customer
                        user.btc_wallet = user.btc_wallet + float(quantity)
                        user.dollar_wallet = user.dollar_wallet
                        customer.profit += price
                        user.profit -= price
                        customer.save()
                        user.save()
                        messages.success(request, f'You have a match. Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $')
                        my_coll = mydb['Customer sell an equal order to buy']
                        order_to_sell_transaction = {
                            'Buyer': customer.user.username,
                            'Buyer Id': customer.pk,
                            'Buyer $ amount before transaction': order.customer.dollar_wallet + price,
                            'Buyer $ amount after transaction': order.customer.dollar_wallet,
                            'Buyer btc amount before transaction': order.customer.btc_wallet - quantity,
                            'Buyer btc amount after transaction': order.customer.btc_wallet,
                            'Order price': price,
                            'Order quantity': quantity,
                            'Seller': order.customer.user.username,
                            'Seller id': order.customer.pk,
                            'Seller btc Balance before transaction': order.customer.btc_wallet + quantity,
                            'Seller btc Balance after transaction': order.customer.btc_wallet,
                            'Seller $ before transaction': order.customer.dollar_wallet - price,
                            'Seller $ after transaction': customer.dollar_wallet,
                            }
                        x = my_coll.insert_one(order_to_sell_transaction)
                        order.delete()
                        return redirect('/homepage/')

                    if quantity == order.quantity and price != order.price :
                        average_max = int(order.price + order.price /100 * 0.3)
                        average = int(order.price)
                        average_min = int(order.price - order.price /100 * 0.3)
                        average_range_max = range(average, average_max)
                        average_range_min = range(average_min, average)

                        if price in average_range_max or price in average_range_min:
                            if order.customer.dollar_wallet >= average_max:
                                customer.dollar_wallet = customer.dollar_wallet + float(price)
                                customer.btc_wallet = customer.btc_wallet - float(quantity)
                                user = order.customer
                                user.btc_wallet = user.btc_wallet + float(quantity)
                                user.dollar_wallet = user.dollar_wallet + float(order.price) - float(price)
                                customer.profit += price
                                user.profit -= price
                                user.save()
                                customer.save()
                                messages.success(request,
                                                 f'You have a match. Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $')
                                my_coll = mydb['Customer sell an average order to buy']
                                order_to_sell_average_transaction = {
                                    'Buyer': order.customer.user.username,
                                    'Buyer Id': order.customer.pk,
                                    'Buyer $ amount before transaction': order.customer.dollar_wallet + price,
                                    'Buyer $ amount after transaction': order.customer.dollar_wallet,
                                    'Buyer btc amount before transaction': order.customer.btc_wallet - quantity,
                                    'Buyer btc amount after transaction': order.customer.btc_wallet,
                                    'Order price': price,
                                    'Order quantity': quantity,
                                    'Seller': customer.user.username,
                                    'Seller id': customer.pk,
                                    'Seller btc Balance before transaction': customer.btc_wallet + quantity,
                                    'Seller btc Balance after transaction': customer.btc_wallet,
                                    'Seller $ before transaction': customer.dollar_wallet - price,
                                    'Seller $ after transaction': customer.dollar_wallet,
                                }
                                x = my_coll.insert_one(order_to_sell_average_transaction)
                                order.delete()
                                return redirect('/homepage/')
                        else:
                            customer.btc_wallet = customer.btc_wallet
                            form.save()
                            messages.success(request,'Your order is in the waiting list (average not good')
                            return redirect('/homepage/')


                    if quantity != order.quantity and price == order.price :
                        if quantity > order.quantity :
                            customer.dollar_wallet = customer.dollar_wallet + float(price)
                            customer.btc_wallet = customer.btc_wallet - float(order.quantity)
                            user = order.customer
                            user.btc_wallet = user.btc_wallet + float(order.quantity)
                            user.dollar_wallet = user.dollar_wallet
                            customer.profit += price
                            user.profit -= price
                            user.save()
                            customer.save()
                            messages.success(request,
                                             f'You have a match less, you spent just {order.quantity} btc and you get {order.price} $'
                                             f'Now your btcBalance is {customer.btc_wallet} and {customer.dollar_wallet} $')

                            my_coll = mydb['Customer sell a different quantity order to buy']
                            order_to_sell_different_quantity_transaction = {
                                'Buyer': order.customer.user.username,
                                'Buyer Id': order.customer.pk,
                                'Buyer $ amount before transaction': order.customer.dollar_wallet + price,
                                'Buyer $ amount after transaction': order.customer.dollar_wallet,
                                'Buyer btc amount before transaction': order.customer.btc_wallet - order.quantity,
                                'Buyer btc amount after transaction': order.customer.btc_wallet,
                                'Order price': price,
                                'Buyer Order Quantity': order.quantity,
                                'Seller Order quantity': quantity,
                                'Matching Order is': order.quantity,
                                'Seller': customer.user.username,
                                'Seller id': customer.pk,
                                'Seller btc Balance before transaction': customer.btc_wallet + order.quantity,
                                'Seller btc Balance after transaction': customer.btc_wallet,
                                'Seller $ before transaction': customer.dollar_wallet - price,
                                'Seller $ after transaction': customer.dollar_wallet,
                                }
                            x = my_coll.insert_one(order_to_sell_different_quantity_transaction)
                            order.delete()
                            return redirect('/homepage/')
                        else:
                            customer.btc_wallet = customer.btc_wallet
                            form.save()
                            customer.save()
                            messages.success(request, 'Your order is in the waiting list')
                            return redirect('/homepage/')

                else:
                    order = OrderToSell(customer=customer, price=price, quantity=quantity)
                    customer.btc_wallet = customer.btc_wallet - float(quantity)
                    order.save()
                    customer.save()
                    messages.success(request, 'Your order is in the waiting list new order')
                    return redirect('/homepage/')


            else:
                messages.error(request, "You don't have necessary funds")
                return redirect('/homepage/')

    else:
        form = PublishOrderToSell()
        context = {'form': form}
        return render(request, 'publish_order_to_sell.html', context)