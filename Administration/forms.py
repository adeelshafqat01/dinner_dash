from django import forms
from django.forms import ModelForm
from Order.models import Item
from django.core.exceptions import ObjectDoesNotExist


class AddItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'price', 'status', 'photo_url')
        help_texts = {'username': None}

    def clean(self):
        price = self.cleaned_data.get("price")
        title = self.cleaned_data.get("title")
        if price <= 0:
            raise forms.ValidationError("Price Cant be 0")
        try:
            Item.objects.get(title=title)
        except ObjectDoesNotExist:
            pass
        else:
            raise forms.ValidationError("Item Already Exists")


class ModifyItemForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Item
        fields = ('id', 'title', 'description', 'price', 'status', 'photo_url')
        help_texts = {'username': None}

    def clean(self):
        status = self.cleaned_data.get("status")
        title = self.cleaned_data.get("title")
        id = self.cleaned_data.get("id")
        if not title:
            raise forms.ValidationError("Title Needed")
        if not status:
            raise forms.ValidationError("Status Needed")
        try:
            item = Item.objects.get(id=id)
        except ObjectDoesNotExist:
            pass
        else:
            if title == item.title:
                pass
            else:
                try:
                    item = Item.objects.get(title=title)
                except ObjectDoesNotExist:
                    pass
                else:
                    raise forms.ValidationError(
                        "Sorry You cant use this title")
