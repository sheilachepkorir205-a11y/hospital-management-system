from urllib.parse import urlparse

from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render

from .auth import SESSION_USER_ID, get_authenticated_user
from .models import User


def login_view(request):
    if get_authenticated_user(request) is not None:
        return redirect(request.GET.get('next') or 'patient-list')

    next_url = request.POST.get('next') or request.GET.get('next') or ''
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = User.objects.filter(
            is_active=True,
        ).filter(
            username=username,
        ).first() or User.objects.filter(
            is_active=True,
            email=username.lower(),
        ).first()
        if user and check_password(password, user.password_hash):
            if not _is_safe_next_url(next_url):
                next_url = ''
            request.session.flush()
            request.session[SESSION_USER_ID] = user.user_id
            request.session.set_expiry(60 * 60 * 8)
            return redirect(next_url or 'patient-list')
        messages.error(request, 'Invalid username or password.')

    return render(request, 'index.html', {'next': next_url})


def logout_view(request):
    if request.method == 'POST':
        request.session.flush()
        return redirect('login')
    return redirect('patient-list')


def _is_safe_next_url(value):
    parsed = urlparse(value)
    return bool(value) and not parsed.netloc and not parsed.scheme and value.startswith('/')