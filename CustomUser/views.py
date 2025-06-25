from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import CustomAuthenticationForm, CustomUserCreationForm

def registerView(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            login(request, form.save())
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, "registration/signup.html", {'form': form})

def loginView(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_superuser:
                return redirect(admin)
            else:
                return redirect(home)
    else:
        form = CustomAuthenticationForm()
    return render(request, "registration/login.html", {'form': form})

def home(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect(admin)
    return render(request, "index/UserPage.html")

def admin(request):
    if request.user.is_superuser:
        return render(request, "index/AdminPage.html")
    else:
        return redirect(home)