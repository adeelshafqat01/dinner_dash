from django.urls import path
from .views import ViewCart, AddToCart, RemoveFromCart
urlpatterns = [
    path('viewcart/', ViewCart.as_view(), name="CartView"),
    path('addtocart/<int:id>', AddToCart.as_view(), name="addtocart"),
    path('removefromcart/', RemoveFromCart.as_view(),
         name="removefromcart")
]
