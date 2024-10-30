from django.urls import path
from . import views

urlpatterns = [
    path('', views.base_message, name='base_message'),
    path('add_user/', views.add_user, name='add_user'),
    path('delete_user/<int:uni>/', views.delete_user, name='delete_user'),
    path('get_all_users/', views.get_all_users, name='get_all_users'),
    path('get_one_user/', views.check_user_password, name='get_one_user'),
]
