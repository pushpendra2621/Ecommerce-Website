from store.utils import cookieCart
from django.shortcuts import render
from store.models import *
from django.http import JsonResponse
import json
import datetime
from django.db.models import Q

from . utils import cookieCart, cartData, guestOrder

# Create your views here.

def store(request):

	cart = cartData(request)
	cartItems = cart["cartItems"]
		
	products = Product.objects.all()

	## Search Functionality
	query= request.GET.get('q')
	if query is not None:
		lookups= Q(name__icontains=query) | Q(id__icontains=query)
		products= products.filter(lookups).distinct()

	context = {"products":products,
				"cartItems":cartItems
			}
	return render(request, "store.html", context)

def cart(request):

	cart = cartData(request)
	items = cart["items"]
	order = cart["order"]
	cartItems = cart["cartItems"]
		
	context = {
		'items':items,
		'order':order,
		"cartItems":cartItems
	}
	return render(request, "cart.html", context)

def checkout(request):
	
	cart = cartData(request)
	items = cart["items"]
	order = cart["order"]
	cartItems = cart["cartItems"]

	context = {
		'items':items,
		'order':order,
		"cartItems":cartItems
	}
	return render(request, "checkout.html", context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('product ID ', productId)
	print('Action', action)
	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete =False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product= product)

	if action == "add":
		orderItem.quantity += 1
	elif action== "remove":
		orderItem.quantity -= 1

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item has been added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete =False)

	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id
	
	if total == float(order.get_cart_total):
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAdress.objects.create(
			customer = customer,
			order = order,
			address = data['shipping']['address'],
			city = data['shipping']['city'],
			state = data['shipping']['state'],
			zipcode = data['shipping']['zipcode'],
		)

	return JsonResponse('Payment successfull!', safe=False)
