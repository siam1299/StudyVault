# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # user তৈরি হলো

            # ✅ নতুন ৩ লাইন: backend resolve হবে
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=user.username, password=raw_password)
            login(request, user)  # backend এখন সেট আছে

            messages.success(request, "Account created successfully!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Logged in successfully!")
            return redirect('home')
    else:
        form = AuthenticationForm(request)
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect('home')
