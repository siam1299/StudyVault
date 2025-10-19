from django.db import models
from django.contrib.auth.models import User

def avatar_upload_path(instance, filename):
    # media/avatars/<username>/<filename>
    return f"avatars/{instance.user.username}/{filename}"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # 🖼 image path fix
    avatar = models.ImageField(upload_to=avatar_upload_path, blank=True, null=True)

    # 📚 basic info
    university = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    # 🆕 নতুন ফিল্ড
    subject = models.CharField(max_length=255, blank=True, null=True)
    bio     = models.TextField(max_length=400, blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"
