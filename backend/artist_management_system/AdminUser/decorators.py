from functools import wraps
from django.shortcuts import redirect


def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.session.get('user_id'):
            return redirect('login_page')
        return view_func(request, *args, **kwargs)
    return wrapper

