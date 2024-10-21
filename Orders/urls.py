from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('cart/', views.show_cart, name='cart'),
    path('orders', views.show_orders, name='orders'),

    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('remove_item/<pk>/', views.remove_item_from_cart, name='remove_item'),
    path('checkout/<int:pk>/', views.checkout_cart, name='checkout'),  # Ensure this is defined
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
