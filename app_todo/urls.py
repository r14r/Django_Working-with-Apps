from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views
from .api_views import TodoItemViewSet

app_name = 'app_todo'

router = DefaultRouter()
router.register(r'', TodoItemViewSet, basename='todo-api')

urlpatterns = [
    path('', views.todo_list, name='list'),
    path('new/', views.todo_create, name='create'),
    path('<int:pk>/edit/', views.todo_update, name='update'),
    path('<int:pk>/delete/', views.todo_delete, name='delete'),
    path('<int:pk>/toggle/', views.todo_toggle, name='toggle'),
    path('api/', include(router.urls)),
]
