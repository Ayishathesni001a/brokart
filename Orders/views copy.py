from django.shortcuts import render,redirect
from .models import Order,OrderedItem
from Products.models import Product

# Create your views here.
def show_cart(request):
    return render(request,'cart.html')
def add_to_cart(request):
    if request.POST:
        user=request.user
        customer=user.customer_profile
        quantity=request.POST.get('quantity')
        product_id=request.POST.get('product_id')
        size=request.POST.get('size')
        cart_obj,created=Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )
        product=Products.objects.get(pk=product_id)
        ordered_item=OrderedItem.objects.create(
            product=product,
            owner=cart_obj,
            quantity=quantity,
            size=size
        )
        return redirect('cart')

