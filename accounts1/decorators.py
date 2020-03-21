from django.http import HttpResponse
from django.shortcuts import render, redirect,  get_object_or_404
# a decorator is a function that takes in another function
# as a parameter and lets us add a little functionality before
# the original function is called
def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('accounts1:home')
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def allowed_user(allowed_rolls = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_rolls:

                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('You are not authorised to view this page')
        return wrapper_func
    return decorator
def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('accounts1:user-page')
        if group == 'admin':
            return  view_func(request, *args, **kwargs)
    return wrapper_func
