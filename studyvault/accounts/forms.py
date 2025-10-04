# accounts/forms.py
from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "hidden",   # 👈 হাইড করে দিবে, শুধু hover label-এ কাজ হবে
            "accept": "image/*"
        })
    )

    class Meta:
        model = UserProfile
        fields = ["avatar", "university", "department"]
        widgets = {
            "university": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "Enter your university"  # ✅ এখানে ডিফল্ট ভ্যালু দেখাবে না
            }),
            "department": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "Enter your department"
            }),
        }
