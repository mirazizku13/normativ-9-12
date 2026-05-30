from django.urls import path
from . import views

urlpatterns = [
    path('', views.list, name='list_order'),
    path('add/', views.add, name='add_order'),
    path('edit/<int:pk>/', views.edit, name='edit_order'),
    path('delete/<int:pk>/', views.delete, name='delete_order'),
]