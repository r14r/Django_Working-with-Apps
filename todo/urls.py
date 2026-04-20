from django.urls import path

from . import views

app_name = 'todo'

urlpatterns = [
    path('', views.todo_list, name='list'),
    path('new/', views.todo_create, name='create'),
    path('<int:pk>/edit/', views.todo_update, name='update'),
    path('<int:pk>/delete/', views.todo_delete, name='delete'),
    path('<int:pk>/toggle/', views.todo_toggle, name='toggle'),
]
