# decorators.py
from django.shortcuts import redirect
from functools import wraps

def login_required_custom(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if 'username' in request.session:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_login_page')
    return _wrapped_view

