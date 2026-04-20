from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('auth/', include('app_auth.urls')),
    path('todos/', include('app_todo.urls')),
    path('app-admin/', include('app_admin.urls')),
]
