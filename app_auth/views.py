import uuid

from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetDoneView
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from .forms import LoginForm, RegisterForm

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'app_auth/login.html'
    authentication_form = LoginForm

    def form_valid(self, form):
        user = form.get_user()
        if not user.email_verified:
            messages.warning(
                self.request,
                'Bitte bestätige zuerst deine E-Mail-Adresse. '
                'Prüfe dein Postfach oder fordere eine neue Bestätigungsmail an.',
            )
            return redirect('app_auth:verify_email_pending')
        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass


class UserPasswordResetView(PasswordResetView):
    template_name = 'app_auth/password_reset.html'
    email_template_name = 'app_auth/password_reset_email.txt'
    subject_template_name = 'app_auth/password_reset_subject.txt'
    success_url = reverse_lazy('app_auth:password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'app_auth/password_reset_done.html'


def register_view(request):
    if request.user.is_authenticated:
        return redirect('app_todo:list')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email_verified = False
            user.email_verification_token = uuid.uuid4()
            user.save()
            _send_verification_email(request, user)
            messages.success(request, 'Registrierung erfolgreich. Bitte bestätige deine E-Mail-Adresse.')
            return redirect('app_auth:verify_email_pending')
    else:
        form = RegisterForm()

    return render(request, 'app_auth/register.html', {'form': form})


def verify_email_pending_view(request):
    return render(request, 'app_auth/verify_email_pending.html')


def verify_email_view(request, token):
    user = get_object_or_404(User, email_verification_token=token)
    if not user.email_verified:
        user.email_verified = True
        user.save(update_fields=['email_verified'])
        messages.success(request, 'E-Mail-Adresse erfolgreich bestätigt. Du kannst dich jetzt einloggen.')
    else:
        messages.info(request, 'Deine E-Mail-Adresse wurde bereits bestätigt.')
    return redirect('app_auth:login')


def resend_verification_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        try:
            user = User.objects.get(email=email, email_verified=False)
            _send_verification_email(request, user)
            messages.success(request, 'Bestätigungsmail wurde erneut versendet.')
        except User.DoesNotExist:
            messages.error(request, 'Keine unbestätigte Registrierung mit dieser E-Mail-Adresse gefunden.')
        return redirect('app_auth:verify_email_pending')
    return render(request, 'app_auth/resend_verification.html')


def _send_verification_email(request, user):
    verify_url = request.build_absolute_uri(
        reverse('app_auth:verify_email', kwargs={'token': str(user.email_verification_token)})
    )

    print(f"verification url={verify_url}")
    
    send_mail(
        subject='E-Mail-Adresse bestätigen',
        message=f'Hallo {user.username},\n\nbitte klicke auf folgenden Link, um deine E-Mail-Adresse zu bestätigen:\n\n{verify_url}\n\nDiesen Link nur einmalig verwenden.',
        from_email=None,
        recipient_list=[user.email],
    )
