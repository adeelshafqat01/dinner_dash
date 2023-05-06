from django.forms import ModelForm
from .models import Order


class ChangeOrder(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for myField in self.fields:
            self.fields[myField].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Order
        fields = ('status',)
        help_texts = {'username': None}
