from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
import json
import datetime

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':True}
        cartItems = order['get_cart_items']
        for i in cart:
            cartItems += cart[i]['quantity']
    products = Product.objects.all()
    context = {'products':products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        print('cart: ',cart)

        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':True}
        cartItems = order['get_cart_items']

        for i in cart:
            cartItems += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])

            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']

            item = {
                'product':{
                    'id':product.id,
                    'name':product.name,
                    'price':product.price,
                    'imageURL':product.imageURL
                },
                'quantity':cart[i]['quantity'],
                'get_total':total
            }
            items.append(item)

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        items = []
        order = {'get_cart_items':0, 'get_cart_total':0, 'shipping':True}
        cartItems = order['get_cart_items']
        for i in cart:
            order['get_cart_items'] += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = product.price * cart[i]['quantity']     

            item = {
                'product':{
                    'id':product.id,
                    'imageURL':product.imageURL,
                    'price':product.price,
                    'name':product.name
                },
                'quantity':cart[i]['quantity'],
                'get_total': total
            }
            order['get_cart_total'] += total
            cartItems += cart[i]['quantity'] 
            items.append(item)

        
    context = {'items':items, 'order':order,'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("item was added", safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        total = float(data['form']['total'])
        order, created = Order.objects.get_or_create(customer=customer,complete=False)
        order.transaction_id = transaction_id

    else:
        name = data['form']['user']
        email = data['form']['email']

        customer, created = Customer.objects.get_or_create(email=email)
        order = Order.objects.create(transaction_id=transaction_id)
        total = float(data['form']['total'])
        customer.name = name
        customer.save()
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart={}

        items = []
        for i in cart:
            product = Product.objects.get(id=i)

            item = {
                'product':{
                    'id':product.id,
                    'imageURL':product.imageURL,
                    'price':product.price,
                    'name':product.name
                },
                'quantity':cart[i]['quantity'],
                'get_total': cart[i]['quantity']
            }
            items.append(item)

        for item in items:
            product = Product.objects.get(id=i)
            OrderItem.objects.create(product=product,
                order=order,
                quantity=item['quantity'],
                date_added=transaction_id)
 
        
    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer = customer,
            order = order,
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zip_code = data['shipping']['zip_code']
        )

    return JsonResponse("payment complete", safe=False)

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('store')
    else:
        form = UserCreationForm()
    return render(request, 'store/signup.html', {'form':form})
    
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('store')
    else:
        form = AuthenticationForm()
    return render(request, 'store/login.html', {'form':form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('store')