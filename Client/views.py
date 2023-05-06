from django import http
from django.views.generic.list import ListView
from Order.models import Category, Item
from django.contrib.auth import logout
from django.shortcuts import render
from django.http import JsonResponse
from django.http import HttpResponse
from django.views import View
from .serializers import ItemSerializer
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


class HomePage(ListView):
    model = Item
    paginate_by = 100
    template_name = 'UserHomePage.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, 'error.html')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        if self.request.user.is_superuser:
            logout(self.request)
        return super().get_context_data(**kwargs)


class ViewItem(ListView):
    model = Item
    template_name = 'viewitem.html'

    def get_queryset(self):
        id = self.kwargs['pk']
        try:
            Item.objects.get(id=id)
        except ObjectDoesNotExist:
            return HttpResponse('Item Does not exist')
        else:
            return Item.objects.get(id=id)


class ItemsCategory(View):
    def get(self, request):
        name = request.GET.get('Search')
        if not name:
            return JsonResponse({'error': 'Search field cant be empty'}, safe=False)

        items = Item.objects.filter(title__startswith=name, status='active')
        if items:
            serializer = ItemSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            category = Category.objects.filter(
                Name__startswith=name).prefetch_related('items')
            if category:
                item = category[0].items.all()
                serializer = ItemSerializer(item, many=True)
                return JsonResponse(serializer.data, safe=False)
            else:
                return JsonResponse({'error': 'No item exists'}, safe=False)
