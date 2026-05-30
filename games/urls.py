from django.urls import path
from . import views

app_name = 'games'

urlpatterns = [
    # path('game_list/', views.game_list, name='game_list'),
    path('list/', views.GameListView.as_view(), name='game_list'),
    path('<int:id>/', views.game_detail, name='game_detail'),
    # path('create/', views.game_create, name='game_create'),
    path('create/', views.GamesCreateView.as_view(), name='game_create'),
    # path('<int:id>/edit/', views.game_update, name='game_update'),
    path('<int:pk>/edit/', views.GamesUpdateView.as_view(), name='game_update'),
    # path('<int:id>/delete/', views.game_delete, name='game_delete'),
    path('<int:pk>/delete/', views.GamesDeleteView.as_view(), name='game_delete'),
    path('published/<int:pk>/', views.game_published, name='game_published'),
    path('send-email/', views.SendEmailView.as_view(), name='send_email'),
]

# urlpatterns = [
#     path('list/', views.book_list, name='book_list'),
#     path('detail/<int:pk>/', views.book_detail, name='book_detail'),
#     path('create-form/', views.book_create_form, name='book_create_form'),
#     path('create/', views.book_create, name='book_create'),
#     path('update-form/<int:pk>/', views.book_update_forme, name='book_update_form'),
#     path('update/<int:pk>/', views.book_update, name='book_update'),
#     path('delete/<int:pk>/', views.book_delete, name='book_delete'),
# ]