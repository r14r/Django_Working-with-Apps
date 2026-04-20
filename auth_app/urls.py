from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetCompleteView

from .views import (
    UserLoginView,
    UserLogoutView,
    UserPasswordResetDoneView,
    UserPasswordResetView,
    register_view,
)

app_name = 'auth_app'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password-reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', UserPasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        'reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='auth_app/password_reset_confirm.html', success_url=reverse_lazy('auth_app:password_reset_complete')),
        name='password_reset_confirm',
    ),
    path(
        'reset/complete/',
        PasswordResetCompleteView.as_view(template_name='auth_app/password_reset_complete.html'),
        name='password_reset_complete',
    ),
]
