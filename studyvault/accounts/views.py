# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required   # ✅ দরকার edit_profile এর জন্য

from .models import UserProfile
from .forms import ProfileForm

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # user তৈরি হলো

            raw_password = form.cleaned_data.get("password1")
            user = authenticate(request, username=user.username, password=raw_password)
            login(request, user)

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

@login_required
def my_profile(request):
    # প্রোফাইল না থাকলে বানিয়ে দিই
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Profile updated successfully!")
            return redirect("my_profile")  # একই পেইজে ফিরে আসবে
    else:
        form = ProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        "form": form,
        "profile": profile,
    })
