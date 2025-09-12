# studyvault/views.py
from django.shortcuts import render
from django.db.models import Count
from materials.models import University  # ✅ import

def home(request):
    # Top universities by document count (ties -> by name)
    top_unis = (
        University.objects
        .annotate(num_materials=Count("materials"))
        .order_by("-num_materials", "name")[:12]   # ১২টা দেখাবো
    )
    return render(request, "home.html", {"top_unis": top_unis})
