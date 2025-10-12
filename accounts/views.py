from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomRegisterForm, CustomLoginForm

# 🟢 Register View
def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! Your journey begins 🌱")
            return redirect('dashboard:index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomRegisterForm()

    return render(request, 'accounts/register.html', {'form': form})

# 🟢 Login View
def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard:index')

    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {user.username} 🌿")
                return redirect('dashboard:index')
        messages.error(request, "Invalid username or password.")
    else:
        form = CustomLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

# 🟢 Logout View
def logout_view(request):
    logout(request)
    messages.info(request, "You’ve been logged out successfully. See you soon 🌼")
    return redirect('accounts:login')

# 🟢 Profile View
@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')
