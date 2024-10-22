from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderedItem

class OrderAdmin(admin.ModelAdmin):
    list_filter =[
        "owner",
         "order_status",
         
    ]
    search_fields =[
        "owner",
        "id",
    ]

    
    

admin.site.register(Order,OrderAdmin)

