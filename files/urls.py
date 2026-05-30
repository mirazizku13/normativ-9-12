from django.urls import path
from  . import views
from files.admin import DocumentAdmin

urlpatterns = [
    path('list/', views.files_list, name='files_list'),
    path('create/', views.files_create, name='files_create'),
    path('update/<int:pk>/', views.files_update, name='files_update'),
    path('delete/<int:pk>/', views.files_delete, name='files_delete'),

]