from functools import wraps

from django.contrib import messages
from django.shortcuts import redirect


def email_verified_required(view_func):
    """Decorator that requires a logged-in user with a verified email address."""

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('auth_app:login')
        if not request.user.email_verified:
            messages.warning(request, 'Bitte bestätige zuerst deine E-Mail-Adresse.')
            return redirect('auth_app:verify_email_pending')
        return view_func(request, *args, **kwargs)

    return wrapper
