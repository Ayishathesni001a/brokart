from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderedItem
from Customers.models import Customer  # Ensure this import is present
from django.contrib.auth.decorators import login_required
from Products.models import Product


def show_cart(request):
    user = request.user
    
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('login')

    try:
        customer = user.customer_profile  # Try to get the customer profile
    except Customer.DoesNotExist:
        messages.error(request, "You need to create a customer profile first.")
        return redirect('create_profile')  # Redirect to profile creation view

    # Get or create the cart object
    cart_obj, created = Order.objects.get_or_create(
        owner=customer,
        order_status=Order.CART_STAGE
    )

    # Retrieve ordered items associated with the cart
    ordered_items = OrderedItem.objects.filter(order=cart_obj)

    # Calculate subtotal or other necessary values if needed
    subtotal = sum(item.quantity * item.product.price for item in ordered_items)  # Example calculation

    context = {
        'cart': cart_obj,
        'ordered_items': ordered_items,  # Add ordered items to context
        'subtotal': subtotal,  # Include subtotal if calculated
    }
    
    return render(request, 'cart.html', context)

def remove_item_from_cart(request, pk):
    item = get_object_or_404(OrderedItem, pk=pk)  # Use get_object_or_404 for better error handling
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order

def checkout_cart(request, pk):
    if request.method == 'POST':
        user = request.user
        
        if not user.is_authenticated:
            messages.error(request, "You need to be logged in to proceed.")
            return redirect('login')

        try:
            customer = user.customer_profile  # Ensure the customer profile exists
        except Customer.DoesNotExist:
            messages.error(request, "You need to create a customer profile first.")
            return redirect('create_profile')

        order_obj = get_object_or_404(Order, pk=pk, owner=customer)

        # Calculate total price based on ordered items
        order_obj.total_price = sum(item.product.price * item.quantity for item in order_obj.ordered_items.all())
        order_obj.order_status = Order.ORDER_CONFIRMED
        
        order_obj.save()

        messages.success(request, "Your order has been processed. Your items will be delivered within 2 days.")
        return redirect('checkout')  # Redirect to a confirmation page

    return redirect('cart')  # Handle non-POST requests


@login_required(login_url='account')
def show_orders(request):
    user = request.user
    
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('login')

    try:
        customer = user.customer_profile  # Try to get the customer profile
    except Customer.DoesNotExist:
        messages.error(request, "You need to create a customer profile first.")
        return redirect('cart')  # Redirect to profile creation view

    
    all_orders=Order.objects.filter(owner=customer).exclude(order_status=Order.CART_STAGE)
    context={'orders':all_orders}
    
    return render(request, 'orders.html', context)



@login_required(login_url='account')
def view_orders(request):
    user = request.user
    
    if not user.is_authenticated:
        messages.error(request, "You need to be logged in to view your cart.")
        return redirect('login')

    try:
        customer = user.customer_profile  # Try to get the customer profile
    except Customer.DoesNotExist:
        messages.error(request, "You need to create a customer profile first.")
        return redirect('create_profile')  # Redirect to profile creation view

    
    
    return render(request, 'cart.html')




# Make sure to import your models
@login_required(login_url='account')

def add_to_cart(request):
    if request.method == 'POST':
        user = request.user
        
        if not user.is_authenticated:
            messages.error(request, "You need to be logged in to add items to the cart.")
            return redirect('login')

        try:
            customer = user.customer_profile
        except Customer.DoesNotExist:
            messages.error(request, "You need to create a customer profile first.")
            return redirect('create_profile')

        product_id = request.POST.get('product_id')
        size = request.POST.get('size')
        quantity = float(request.POST.get('quantity', 1))  # Default to 1 if not provided

        try:
            # Get the product instance
            product_instance = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            messages.error(request, "Product not found.")
            return redirect('home')

        # Get or create cart object
        cart_obj, created = Order.objects.get_or_create(
            owner=customer,
            order_status=Order.CART_STAGE
        )

        # Create the ordered item
        ordered_item = OrderedItem.objects.create(
            product=product_instance,  # Pass the Product instance
            order=cart_obj,
            size=size,
            quantity=quantity,
        )
        if created:
            ordered_item.quantity=quantity
            ordered_item.save()
        else:
            ordered_item.quantity=ordered_item.quantity+quantity
            ordered_item.save()

        messages.success(request, f"Added {quantity} of {product_instance.title} (Size: {size}) to your cart.")
        
        # Redirect to the cart page
        return redirect('cart')  # Ensure 'cart' URL takes the user to the cart
        
    return redirect('home')  # Handle non-POST requests
