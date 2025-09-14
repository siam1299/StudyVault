# accounts/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from materials.models import University, Department  # আগের মডেলগুলো reuse

def avatar_upload_path(instance, filename):
    return f"avatars/{instance.user.username}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    # ✅ ForeignKey বাদ দিয়ে CharField ব্যবহার
    university = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"