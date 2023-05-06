from django.urls import reverse
from django.views.generic.list import ListView
from Order.models import Category, Item, Order
from .forms import AddItemForm, ModifyItemForm
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.views.generic.edit import UpdateView
from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import HttpResponseRedirect
from django.contrib import messages
from django.http import HttpResponse
# Create your views here.


class DashBoard(ListView):
    model = Order
    template_name = 'DashBoard.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        elif request.user.is_authenticated:
            return render(request, 'error.html')
        else:
            return HttpResponseRedirect(reverse('loginx'))

    def get_queryset(self):
        completed = []
        placed = []
        canceled = []
        orders = Order.objects.all()
        for order in orders:
            if order.status == 'completed':
                completed.append(order)
            elif order.status == 'canceled':
                canceled.append(order)
            else:
                placed.append(order)
        context = {}
        context['completed'] = completed
        context['placed'] = placed
        context['canceled'] = canceled
        return context


class AddItem(FormView):

    form_class = AddItemForm
    template_name = 'AddItem.html'

    def get_success_url(self):
        messages.success(self.request, 'Item Added Successfully')
        return reverse_lazy('modifyitems')

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'error.html')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Categories'] = Category.objects.all()
        return context

    def form_valid(self, form):
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        price = form.cleaned_data['price']
        status = form.cleaned_data['status']
        url = form.cleaned_data['photo_url']
        categories = self.request.POST.get('browser')
        try:
            c1 = Category.objects.get(Name=categories)
        except ObjectDoesNotExist:
            category = Category.objects.create(Name=categories)
        else:
            category = c1
        item = Item.objects.create(
            title=title, description=description, price=price,
            status=status, photo_url=url)
        category.items.add(item)
        return super().form_valid(form)


class ModifyItem(ListView):
    model = Item
    template_name = 'ModifyItem.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'error.html')


class ModifySingleItem(UpdateView):
    model = Item
    form_class = ModifyItemForm
    template_name = 'modifysingleitem.html'

    def get_success_url(self):
        messages.success(self.request, 'Item Modified Successfully')
        return reverse_lazy('modifyitems')

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        id = self.kwargs['pk']
        ids = Item.objects.filter(id=id)
        if ids:
            if request.user.is_superuser:
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'error.html')
        else:
            return HttpResponse('Item Does not exist')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs['pk']
        categories = Item.objects.get(id=id).items.all()
        print(categories)
        categorees = []
        for category in categories:
            categorees.append(category.Name)
        context['categories'] = categorees
        return context

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ListOrders(ListView):
    model = Order
    template_name = 'ListOrders.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'error.html')

    def get_queryset(self):
        status = self.kwargs['status']
        return Order.objects.filter(status=status)
