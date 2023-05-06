from django.urls import path
from .views import HomePage, ViewItem, ItemsCategory

urlpatterns = [
    path('', HomePage.as_view(), name='homepage'),
    path('itemcategory/', ItemsCategory.as_view(), name='finditems'),
    path('item/<int:pk>', ViewItem.as_view(), name='viewitem')
]
