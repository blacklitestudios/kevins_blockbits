from django.shortcuts import render, redirect
from django import forms
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, TransferForm, CustomLoginForm

from django.contrib.auth import get_user_model
User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            print("EEE")
            user = form.save()
            user.balance = 100
            user.save(update_fields=['balance'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    error = None
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            error = "Invalid credentials"
    else:
        form = CustomLoginForm()
    print(form, flush=True)
    return render(request, 'registration/login.html', {'form': form, 'error': error})


def home(request):
    if False:
        return render(request, 'registration/home.html')
    else:
        return redirect('dashboard')

@login_required
def dashboard(request):
    error = None
    if request.method == 'POST':

        form = TransferForm(request.POST, user=request.user)
    
        if form.is_valid():
            try:
                form.save()
            except forms.ValidationError as e:
                error = str(e)
                pass
    else:
        form = TransferForm(user=request.user)

    if error:
        return render(request, 'registration/dashboard.html', {'form': form, 'error': str(error)}) 
    return render(request, 'registration/dashboard.html', {'form': form})

def profile(request):
    return redirect('dashboard')

def custom_logout(request):
    logout(request)
    return redirect('home')