from django.shortcuts import render, redirect, get_object_or_404

from order.models import Order

from order.forms import OrderModelForm
# Create your views here.
def list(request):
    orders = Order.objects.all()
    return render(request, 'order/list.html', {'orders': orders})


def add(request):
    form = OrderModelForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('list_order')
    return render(request, 'order/create.html', {'form': form})


def edit(request, pk=None):
    order = Order.objects.get(pk=pk)
    if request.method == 'POST':
        form = OrderModelForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('list_order')
    else:
        form = OrderModelForm(instance=order)
    return render(request, 'order/update.html', {'form': form})


def delete(request, pk=None):
    Order.objects.filter(pk=pk).delete()
    return redirect('list_order')
