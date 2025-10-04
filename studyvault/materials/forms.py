# materials/forms.py
from django import forms
from .models import Material
from .models import Material, Comment


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "title",
            "description",
            "university",  # new
            "category",
            "department",
            "semester",
            "file",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. DSA Chapter 3 Notes"}),
            "description": forms.Textarea(attrs={"rows": 4, "placeholder": "Short summary or keywords"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Optional: nice labels
        self.fields["title"].label = "Title"
        self.fields["description"].label = "Description"
        self.fields["category"].label = "Category"
        self.fields["department"].label = "Department"
        self.fields["semester"].label = "Semester/Year"
        self.fields["file"].label = "Upload file"

# ⬇️ নতুন CommentForm (ব্রাউজ পেজে কমেন্ট পোস্ট করার জন্য)
class CommentForm(forms.ModelForm):
    body = forms.CharField(
        label="",
        widget=forms.Textarea(attrs={
            "rows": 2,
            "placeholder": "Write a comment…",
            "class": "w-full border rounded px-3 py-2 text-sm"
        })
    )

    class Meta:
        model = Comment
        fields = ["body"]