# accounts/forms.py
from django import forms
from .models import UserProfile

class ProfileForm(forms.ModelForm):
    # hidden file input (তোমার আগের মতই)
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            "class": "hidden",
            "accept": "image/*",
        })
    )

    class Meta:
        model = UserProfile
        fields = ["avatar", "university", "department", "subject", "bio"]
        widgets = {
            "university": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "Enter your university",
            }),
            "department": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "Enter your department",
            }),
            "subject": forms.TextInput(attrs={
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "What do you study? (e.g., ML, AI, Networking)",
            }),
            "bio": forms.Textarea(attrs={
                "rows": 3,
                "class": "border rounded px-3 py-2 w-full",
                "placeholder": "Write something about yourself...",
            }),
        }
        labels = {
            "bio": "About you",
        }
