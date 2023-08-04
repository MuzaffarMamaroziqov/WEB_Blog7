from django.shortcuts import render
from django.views.generic import  ListView,DetailView, CreateView,DeleteView,UpdateView
from .models import *
from django.urls import reverse_lazy
from django.http import JsonResponse
import json

def SearchPage(request):
    if request.method=='POST':
        searched=request.POST['searched']
        products=OnlineShopModel.objects.filter(title__contains=searched)
        return render(request,'search_post.html',{'searched':searched,'products':products})
    else:
        return render(request,'search_post.html',{'searched': searched })



# class ListViewPage(ListView):
#     model = OnlineShopModel
#     template_name = 'home.html'


class DetailViewPage(DetailView):
    model=OnlineShopModel
    template_name = 'detail_post.html'
    context_object_name = 'product'

class CreateViewPage(CreateView):
    model = OnlineShopModel
    template_name = "create_newpost.html"
    fields = ['title', 'body', 'author' , 'picture', 'price']
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)


class DeleteViewPage(DeleteView):
    model = OnlineShopModel
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')

class UpdateViewPage(UpdateView):
    model = OnlineShopModel
    template_name = 'update_post.html'
    fields = ['title', 'body',  'picture', 'price']
    success_url = reverse_lazy('home')

class OrderViewPage(DetailView):
    model = OnlineShopModel
    template_name = 'buyurtma.html'
    context_object_name = 'post'

def store(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems=order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0 , 'get_cart_total':0}
        cartItems=order['get_cart_items']

    products=OnlineShopModel.objects.all()
    context={'items':items, 'products': products, 'cartItems':cartItems}
    return render(request, 'home.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0 , 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context={'items':items, 'order':order , 'cartItems':cartItems}
    return render(request, 'cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer, complete=False)
        items=order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items=[]
        order={'get_cart_items':0 , 'get_cart_total':0}
        cartItems = order['get_cart_items']
    context={'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = OnlineShopModel.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)