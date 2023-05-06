from datetime import datetime
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.http import HttpResponse
from Authentication.models import User
from Order.models import Order, Item
from Cart.models import Cart
from django.views import View
from django.urls import reverse_lazy
from .forms import ChangeOrder
from django import http
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class PlaceOrder(ListView):
    model = User
    template_name = 'CheckOut.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            if not request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'error.html')
        else:
            return render(request, 'error.html')

    def get_queryset(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        cart = Cart.objects.filter(user=user).prefetch_related('items').all()
        context['items'] = cart[0].items.all()
        total_price = 0
        for item in cart[0].items.all():
            total_price += item.price
        context['totalprice'] = total_price
        return context


class FinalizeOrder(View):
    def get(self, request, price):
        if self.request.user.is_authenticated:
            if not self.request.user.is_superuser:
                user = self.request.user
                cart = Cart.objects.filter(
                    user=user).prefetch_related('items').all()
                pric = int(float(price))
                order1 = Order.objects.create(
                    date_time=datetime.now(), user=user, total_price=pric,
                    status='placed')
                for item in cart[0].items.all():
                    order1.items.add(item)
                cart.delete()
                return render(request, 'OrderSuccess.html')
            else:
                return render(request, 'error.html')
        else:
            return render(request, 'error.html')


class ViewOrders(ListView):
    model = Order
    template_name = 'ViewOrders.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'error.html')

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(user=user)


class ViewOrderDetail(ListView):
    model = Item
    template_name = 'orderdetails.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            orders = Order.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponse('Sorry No order exists for This id')
        else:
            if request.user.is_authenticated and (orders.user == request.user or request.user.is_superuser):
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'error.html')

    def get_queryset(self):
        id = self.kwargs['pk']
        order = Order.objects.filter(id=id).prefetch_related('items')
        return order[0].items.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        order = Order.objects.get(id=id)
        if self.request.user.is_superuser:
            user = User.objects.get(id=order.user_id)
            context['username'] = user.username
            context['email'] = user.email
        context['status'] = order.status
        context['price'] = order.total_price
        context['time'] = order.updated_at
        return context


class ChangeOrder(UpdateView):
    model = Order
    form_class = ChangeOrder
    template_name = 'changeorder.html'
    success_url = reverse_lazy('admindashboard')

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        id = self.kwargs['pk']
        try:
            Order.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponse('Sorry No order exists for This id')
        else:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'error.html')

    def form_valid(self, form):
        orderid = self.kwargs['pk']
        status = form.cleaned_data['status']
        order = Order.objects.get(id=orderid)
        if order.status == 'placed':
            return super().form_valid(form)
        elif order.status == 'completed':
            if status == 'placed':
                return HttpResponse('Sorry you can not change the status to placed')
            else:
                return super().form_valid(form)
        elif order.status == 'paid':
            if status == 'canceled':
                return super().form_valid(form)
            else:
                return HttpResponse('Sorry you can not changed placed order except to cancel')
        elif order.status == 'canceled':
            return HttpResponse('Sorry you can not change the canceled')
        return super().form_valid(form)
