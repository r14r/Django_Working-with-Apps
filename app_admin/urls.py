from django.urls import path
from . import views

app_name = 'app_admin'

urlpatterns = [
    path('users/', views.user_list, name='user_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/<int:user_id>/password/', views.user_change_password, name='user_change_password'),
    path('users/<int:user_id>/groups/', views.user_assign_groups, name='user_assign_groups'),
    path('groups/', views.group_list, name='group_list'),
    path('groups/add/', views.group_add, name='group_add'),
    path('groups/<int:group_id>/edit/', views.group_edit, name='group_edit'),
]
