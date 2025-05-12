from django.shortcuts import render, redirect
from django.contrib import messages
from functools import wraps
from django.contrib.auth.hashers import make_password, check_password
from .models import User

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print("CHECKING AUTH")
        if not request.session.get('user_id'):
            messages.error(request, 'You have to be logged in to access dashboard')
            return redirect("zoomApp:index")
        return view_func(request, *args, **kwargs)
    return wrapper


def index(request):
    return render(request, 'zoomApp/index.html')

def login_form_partial(request):
    return render(request, 'partials/login_form.html')

def register_form_partial(request):
    return render(request, 'partials/register_form.html')

def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user_password = request.POST.get('password')
        user = User.objects.filter(email=email).first()

        if user and check_password(user_password, user.password):
            request.session['user_id'] = user.id
            return redirect("zoomApp:dashboard")
        else:
            messages.error(request, 'User not found')
            return redirect('zoomApp:index')
    return redirect('zoomApp:index')

def logout(request):
    request.session.flush() 
    messages.success(request, "You have been logged out.")
    return redirect("zoomApp:index")

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        user_password = request.POST.get('password')

        password = make_password(user_password)

        try:
            User.objects.create(username=username, email=email, password=password)
            messages.success(request, 'Registration successful')
            if request.headers.get('Hx-Request'):
                return render(request, 'partials/login_form.html')
            return redirect('zoomApp:index')
        except:
            messages.error(request, 'Registration failed')
            if request.headers.get('Hx-Request'):
                return render(request, 'partials/register_form.html')
            return render(request, 'zoomApp/index.html', {'show_register' : True})
    
@login_required 
def dashboard(request):
    return render(request, 'zoomApp/dashboard.html')
