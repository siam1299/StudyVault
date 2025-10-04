# materials/models.py
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    """
    উদাহরণ: Notes, Assignments, Books, Question Papers
    """
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Department(TimeStampedModel):
    """
    উদাহরণ: CSE, EEE, BBA ইত্যাদি
    """
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SemesterYear(TimeStampedModel):
    """
    উদাহরণ: '1st Semester', '2nd Semester' অথবা 'Year-1', 'Year-2' ইত্যাদি
    ফ্লেক্সিবল রাখতে name ফ্রি-টেক্সট রেখেছি।
    """
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    class Meta:
        verbose_name = "Semester / Year"
        verbose_name_plural = "Semesters / Years"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def validate_file_size(f):
    max_mb = 50
    if f.size > max_mb * 1024 * 1024:
        raise ValidationError(f"File too large. Max size is {max_mb} MB.")


class Material(TimeStampedModel):
    """
    মূল কন্টেন্ট মডেল: কোর্স ফাইল আপলোড
    """
    CATEGORY_CHOICES_HELP = "Examples: Notes, Assignments, Books, Question Papers"

    uploader = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="materials"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    university = models.ForeignKey(  # ✅ নতুন ফিল্ড
        "University",
        on_delete=models.PROTECT,
        related_name="materials",
        null=True, blank=True
    )

    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="materials"
    )
    department = models.ForeignKey(
        Department, on_delete=models.PROTECT, related_name="materials"
    )
    semester = models.ForeignKey(
        SemesterYear, on_delete=models.PROTECT, related_name="materials"
    )

    file = models.FileField(
        upload_to="materials/%Y/%m/",
        validators=[
            FileExtensionValidator(allowed_extensions=[
                "pdf", "doc", "docx", "ppt", "pptx", "xls", "xlsx", "zip"
            ]),
            validate_file_size,
        ],
        help_text="Allowed: pdf, doc(x), ppt(x), xls(x), zip. Max 50MB."
    )

    download_count = models.PositiveIntegerField(default=0)

    # রেটিং/অ্যাপ্রুভাল পরে অ্যাড করব
    # average_rating = models.FloatField(default=0.0)
    # is_approved = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} — {self.uploader}"


class Upvote(TimeStampedModel):
    material = models.ForeignKey(
        "Material",
        on_delete=models.CASCADE,
        related_name="upvotes"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="material_upvotes"
    )

    class Meta:
        # একই user যেন একই material-এ একবারই upvote দিতে পারে
        constraints = [
            models.UniqueConstraint(
                fields=["material", "user"],
                name="unique_upvote_per_user_material"
            )
        ]
        indexes = [
            models.Index(fields=["material"]),
            models.Index(fields=["user"]),
        ]

    def __str__(self):
        return f"{self.user.username} → {self.material.title}"


class Downvote(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="downvotes",
    )
    material = models.ForeignKey(
        "Material",
        on_delete=models.CASCADE,
        related_name="downvotes",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "material")   # একজন ইউজার একই ম্যাটেরিয়াল একবারই downvote দিতে পারবে
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} ↓ {self.material_id}"


class Comment(models.Model):
    material = models.ForeignKey(
        'Material',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='material_comments'
    )
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']  # নতুন কমেন্ট আগে

    def __str__(self):
        return f"Comment by {self.user} on {self.material} ({self.created_at:%Y-%m-%d})"


class University(TimeStampedModel):
    """
    উদাহরণ: University of Dhaka, BUET, Harvard University ইত্যাদি
    """
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=180, unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
