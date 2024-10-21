from django import template

register = template.Library()

@register.simple_tag(name='gettotal')
def gettotal(order):
    total = 0
    for item in order.ordered_items.all():  # Accessing the related ordered items
        total += item.quantity * item.product.price  # Assuming Product has a price field
    return total
