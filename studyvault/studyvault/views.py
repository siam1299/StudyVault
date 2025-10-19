# studyvault/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.db.models import Count
from django.contrib.auth.models import User
from materials.models import University  # ✅ import
from accounts.models import UserProfile
from accounts.forms import ProfileForm

def home(request):
    # Top universities by document count (ties -> by name)
    top_unis = (
        University.objects
        .annotate(num_materials=Count("materials"))
        .order_by("-num_materials", "name")[:12]
    )
    return render(request, "home.html", {"top_unis": top_unis})


@login_required
def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = getattr(profile_user, "profile", None)

    # শুধু owner হলে Edit করতে পারবে
    if request.user == profile_user:
        if request.method == "POST":
            form = ProfileForm(request.POST, request.FILES, instance=profile)
            if form.is_valid():
                form.save()
        else:
            form = ProfileForm(instance=profile)
    else:
        form = None

    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "profile": profile,
        "form": form,
    })
