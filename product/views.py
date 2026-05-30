from urllib import request

from django.shortcuts import render, redirect

import product
from product.forms import ProductForm
from .models import Product


# Create your views here.
def product_list(request):
    prducts = Product.objects.all()
    return render(request, 'product/list.html', {'products': prducts})

def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product/detail.html', {'product': product})

def product_create_from(request):
    return render(request, 'product/create.html')

def product_create(request):
    data =request.POST
    product = Product(title=data['title'], description=data.get("description"), price=data['price'])
    product.save()
    return redirect('product_list')


def product_update_from(request, pk=None):
    product = Product.objects.filter(pk=pk)
    form = ProductForm(instance=product)
    return render(request, 'product/update.html', {'product': product, 'form': form})

def product_update(request, pk=None):
    product = Product.objects.filter(id=pk)
    form = ProductForm(instance=product, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect('product_list')
    return render(request, 'product/update.html', {'form': form, 'product': product})

def product_delete(request, pk):
    Product.objects.filter(pk=pk).delete()
    return redirect('product_list')