from django.forms import ModelForm

from order.models import Order


class OrderModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ('customer_name','phone', 'address', 'total_price', 'status', 'is_paid')