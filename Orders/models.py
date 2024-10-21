
from django.db import models
from Customers.models import Customer
from Products.models import Product

class Order(models.Model):
    LIVE = 1
    DELETE = 0    
    DELETE_CHOICES = ((LIVE, 'Live'), (DELETE, 'Deleted'))
    
    CART_STAGE = 0
    ORDER_CONFIRMED = 1
    ORDER_PROCESSED = 2
    ORDER_DELIVERED = 3
    ORDER_REJECTED = 4
    STATUS_CHOICES = (
        (CART_STAGE, 'Cart'),
        (ORDER_CONFIRMED, 'Order Confirmed'),
        (ORDER_PROCESSED, 'Order Processed'),
        (ORDER_DELIVERED, 'Order Delivered'),
        (ORDER_REJECTED, 'Order Rejected'),
    )
    
    order_status = models.IntegerField(choices=STATUS_CHOICES, default=CART_STAGE)
    total_price = models.FloatField(default=0)
    owner = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, related_name='orders')
    delete_status = models.IntegerField(choices=DELETE_CHOICES, default=LIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "order-{}-{}".format(self.id,self.owner.user.username)

class OrderedItem(models.Model):
    product = models.ForeignKey(Product, related_name='ordered_items', on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='ordered_items')
    size = models.IntegerField(choices=[
        (1, 'S'),
        (2, 'M'),
        (3, 'L'),
        (4, 'XL'),
        (5, 'XXL'),
    ], default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} (Size: {self.size})"
