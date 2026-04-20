from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import LoginForm, RegisterForm


class UserLoginView(LoginView):
    template_name = 'auth_app/login.html'
    authentication_form = LoginForm


class UserLogoutView(LogoutView):
    pass


class UserPasswordResetView(PasswordResetView):
    template_name = 'auth_app/password_reset.html'
    email_template_name = 'auth_app/password_reset_email.txt'
    subject_template_name = 'auth_app/password_reset_subject.txt'
    success_url = reverse_lazy('auth_app:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'auth_app/password_reset_done.html'


def register_view(request):
    if request.user.is_authenticated:
        return redirect('todo:list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registrierung erfolgreich. Du bist jetzt eingeloggt.')
            return redirect('todo:list')
    else:
        form = RegisterForm()

    return render(request, 'auth_app/register.html', {'form': form})
