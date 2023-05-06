from .forms import SignUpForm, LoginForm, UpdateForm
from django.views import View
from .models import User
from django.views.generic.edit import FormView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from Cart.models import Cart
from Order.models import Item
from django.views.generic.edit import UpdateView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django import http
from django.shortcuts import render
# Create your views here.


class LoginForm(FormView):
    template_name = 'SignIn.html'
    form_class = LoginForm

    def get_success_url(self):
        if self.request.user.is_superuser:
            return reverse_lazy('admindashboard')
        else:
            messages.success(self.request, 'Logged In')
            return reverse_lazy('homepage')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        try:
            user = User.objects.get(email=email)
        except ObjectDoesNotExist:
            pass
        else:
            if user.check_password(password) or user.password == password:
                if user.is_superuser:
                    self.success_url = reverse_lazy('admindashboard')
                    login(self.request, user)
                else:
                    try:
                        cart = self.request.session['cart']
                    except:
                        cart = {}
                    if cart:
                        login(self.request, user)
                        try:
                            c1 = Cart.objects.get(user=self.request.user)
                        except ObjectDoesNotExist:
                            c1 = Cart.objects.create(user=self.request.user)
                        for item_id in cart:
                            item = Item.objects.get(pk=item_id)
                            c1.items.add(item)
                    else:
                        login(self.request, user)
                return super().form_valid(form)
            else:
                pass


class SignUpForm(FormView):
    template_name = 'SignUp.html'
    form_class = SignUpForm

    def get_success_url(self):
        messages.success(self.request, 'Signed Up')
        return reverse_lazy('loginx')

    def form_valid(self, form):
        name = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        display_name = form.cleaned_data['last_name']
        is_admin = 0
        # form.cleaned_data['is_superuser']
        user = User.objects.create(username=name, email=email,
                                   password=password,
                                   last_name=display_name,
                                   is_superuser=is_admin)
        if is_admin == 1:
            self.success_url = reverse_lazy('admindashboard')
            login(self.request, user)
        return super().form_valid(form)


class UpdateInfo(UpdateView):
    model = User
    form_class = UpdateForm
    template_name = 'PersonalInfo.html'

    def dispatch(self, request: http.HttpRequest, *args, **kwargs):
        id = self.kwargs['pk']
        if request.user.is_authenticated and request.user.id == id:
            return super().dispatch(request, *args, **kwargs)
        else:
            return render(request, 'error.html')

    def get_success_url(self):
        messages.success(self.request, 'Info Updated')
        if self.request.user.is_superuser:
            return reverse_lazy('admindashboard')
        else:
            return reverse_lazy('homepage')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class LogOut(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('homepage'))


class ForgotPassword(View):
    def get(self, request):
        return HttpResponse('ok')
