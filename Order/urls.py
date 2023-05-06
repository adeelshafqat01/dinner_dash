from django.urls import path
from .views import FinalizeOrder, PlaceOrder, ViewOrders, ViewOrderDetail
from .views import ChangeOrder
urlpatterns = [
    path('placeorder/', PlaceOrder.as_view(), name='placeorder'),
    path('finalize/<price>', FinalizeOrder.as_view(), name='finalizeorder'),
    path('orders/', ViewOrders.as_view(), name='vieworders'),
    path('ordersdetails/<int:pk>',
         ViewOrderDetail.as_view(), name='vieworderdetails'),
    path('changeorder/<int:pk>', ChangeOrder.as_view(), name='ChangeOrder')
]
