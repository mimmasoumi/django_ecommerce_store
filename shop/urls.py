from shop.views import (
    AddToCart,
    CategoryListView, CheckoutView,
    DetailView, IndexView, OrderSummary,
    RemoveFromCart, RemoveSingleFromCart,
    SearchView

)
from django.urls import path

app_name = 'shop'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('detail/<pk>', DetailView.as_view(), name='detail'),
    path('add_to_cart/<slug>', AddToCart.as_view(), name='add_to_cart'),
    path('remove_from_cart/<slug>',
         RemoveFromCart.as_view(), name='remove_from_cart'),
    path('remove_single_from_cart/<slug>', RemoveSingleFromCart.as_view(),
         name='remove_single_from_cart'),
    path('ordersummary/', OrderSummary.as_view(), name='order_summary'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('list/<slug>', CategoryListView.as_view(), name='archive'),
    path('search/', SearchView.as_view(), name='search'),
]
