from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),        # list sahifasi
    path('<int:pk>/', views.product_detail, name='product_detail'),  # detail sahifasi
    path('create-from/', views.product_create_from, name='product_create_from'),
    path('create/', views.product_create, name='product_create'),
    path('update-from/<int:pk>/', views.product_update_from, name='product_update_from'),
    path('update/<int:pk>/', views.product_update, name='product_update'),
    path('delete/<int:pk>/', views.product_delete, name='product_delete'),
]