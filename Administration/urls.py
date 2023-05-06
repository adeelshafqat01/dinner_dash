from django.urls import path
from .views import DashBoard, AddItem, ModifyItem, ModifySingleItem, ListOrders

urlpatterns = [
    path('dashboard/', DashBoard.as_view(), name='admindashboard'),
    path('additem/', AddItem.as_view(), name='additem'),
    path('modifyitem/', ModifyItem.as_view(), name='modifyitems'),
    path('updateinfo/', DashBoard.as_view(), name='updateinfo'),
    path('modifysingleitem/<int:pk>',
         ModifySingleItem.as_view(), name='modifysingleitem'),
    path('listorders/<str:status>', ListOrders.as_view(), name='listorders')
]
