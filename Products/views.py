from django.shortcuts import render, get_object_or_404
from .models import Product
from django.core.paginator import Paginator  # Corrected import

# Create your views here.
def index(request):
    featured_products= Product.objects.order_by('priority')[:4]
    latest_products= Product.objects.order_by('-id')[:4]
    context={
        
        'featured_products':featured_products,
        'latest_products':latest_products

        
    }

    return render(request, 'index.html',context)

def list_products(request):
    page=1
    if request.GET:
        page=request.GET.get('page',1)
    product_list = Product.objects.order_by('-priority') 
    product_Paginator=Paginator(product_list,2 )
    product_list=product_Paginator.get_page(page)
    context = {'products': product_list}  # Use 'products' as the key
    return render(request, 'products_layout.html', context)


def detail_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)  # Get product by ID
    context = {'product': product}
    return render(request, 'product_detail.html', context)
