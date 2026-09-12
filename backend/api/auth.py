from functools import wraps

from django.shortcuts import redirect

from .models import User


SESSION_USER_ID = 'staff_user_id'


def get_authenticated_user(request):
    user_id = request.session.get(SESSION_USER_ID)
    if not user_id:
        return None

    return User.objects.select_related('role').filter(
        user_id=user_id,
        is_active=True,
    ).first()


def staff_login_required(view):
    @wraps(view)
    def wrapped(request, *args, **kwargs):
        user = get_authenticated_user(request)
        if user is None:
            return redirect(f'/login/?next={request.get_full_path()}')
        request.staff_user = user
        return view(request, *args, **kwargs)

    return wrapped