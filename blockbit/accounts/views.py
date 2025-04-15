from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, UserCreationForm, TransferForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print("EEE")
            user = form.save()
            user.balance = 100
            user.save(update_fields=['balance'])
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            # Add error message
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    else:
        if request.user.is_authenticated:
            return redirect('dashboard')
    return render(request, 'login.html')

def home(request):
    return render(request, 'registration/home.html')

@login_required
def dashboard(request):
    if request.method == 'POST':
        form = TransferForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    return render(request, 'registration/dashboard.html')

def custom_logout(request):
    logout(request)
    return redirect('home')