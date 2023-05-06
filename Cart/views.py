from django.views import View
from django.http import JsonResponse
from django.views.generic.list import ListView
from Order.models import Item
from Cart.models import Cart, CartItems
from django import http
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
# Create your views here.


class ViewCart(ListView):
    model = Item
    template_name = 'Cart.html'
    context_object_name = 'orders'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        if request.user.is_superuser:
            return render(request, 'error.html')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_authenticated:
            cart = Cart.objects.filter(
                user=user).prefetch_related('items').all()
            quantities = []
            if cart:
                cart_items = CartItems.objects.filter(cart=cart[0])
                for item in cart_items:
                    quantities.append(item.quantity)
            context['quantities'] = quantities

        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            cart = Cart.objects.filter(
                user=user).prefetch_related('items').all()
            if cart:
                return cart[0].items.all()
            else:
                return []
        else:
            cart = self.request.session.get('cart')
            items = []
            if cart:
                for item in cart:
                    values = list(cart[item].values())
                    ite = {
                        'id': values[0],
                        'title': values[1],
                        'price': values[2],
                        'photo_url': values[3],
                        'quantity': values[4]
                    }
                    items.append(ite)
            return items


class AddToCart(View):
    def post(self, request, id):
        if request.user.is_superuser:
            return render(request, 'error.html')
        try:
            item = Item.objects.get(pk=id)
        except ObjectDoesNotExist:
            return HttpResponse('Sorry No Item exists for this id')
        else:
            if self.request.user.is_authenticated:
                user = self.request.user
                cart = Cart.objects.filter(
                    user=user).prefetch_related('items').all()
                if cart:
                    flag = 0
                    for itm in cart[0].items.all():
                        if itm == item:
                            flag = 1
                            cartitem = CartItems.objects.get(
                                cart=cart[0], item=itm)
                            count = cartitem.quantity
                            count += 1
                            cartitem.quantity = count
                            cartitem.save()
                            break
                    if flag == 0:
                        cart[0].items.add(item)
                else:
                    c1 = Cart.objects.create(user=user)
                    c1.items.add(item)
                # return HttpResponseRedirect(reverse('homepage'))
                return JsonResponse({}, status=200)
            else:
                cart = self.request.session.get('cart')
                if cart:
                    itemm = cart.get(str(item.id))
                    if itemm:
                        cart[str(item.id)]['quantity'] += 1
                    else:
                        cart[item.id] = {'id': str(item.id),
                                         'title': item.title,
                                         'price': item.price,
                                         'url': item.photo_url,
                                         'quantity': 1}
                else:
                    cart = {}
                    cart[item.id] = {'id': str(item.id),
                                     'title': item.title,
                                     'price': item.price, 'url': item.photo_url,
                                     'quantity': 1}
                self.request.session['cart'] = cart
                # return HttpResponseRedirect(reverse('homepage'))
                return JsonResponse({}, status=200)


class RemoveFromCart(View):
    def post(self, request):
        id = request.POST.get('item_id')
        if request.user.is_superuser:
            return render(request, 'error.html')
        if self.request.user.is_authenticated:
            user = self.request.user
            item = Item.objects.get(pk=id)
            cart = Cart.objects.filter(
                user=user).prefetch_related('items').all()
            cart[0].items.remove(item)
            return JsonResponse({}, status=200)
            # return HttpResponseRedirect(reverse('CartView'))
        else:
            try:
                cart = self.request.session['cart']
            except:
                return JsonResponse({}, status=404)
            else:
                cart.pop(str(id))
                self.request.session.clear()
                self.request.session['cart'] = cart
                return JsonResponse({}, status=200)
            # return HttpResponseRedirect(reverse('CartView'))
