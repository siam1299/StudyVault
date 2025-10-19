from django.db import migrations
from django.utils.text import slugify

CATS = [
    ("pdf", "pdf"),
    ("docx", "docx"),
    ("pptx", "pptx"),
    ("semester", "semester"),
    ("subject", "subject"),
    ("department", "department"),
]

def create_core_categories(apps, schema_editor):
    Category = apps.get_model("materials", "Category")
    for name, _ in CATS:
        obj, created = Category.objects.get_or_create(name=name, defaults={"slug": slugify(name)})
        if not created and not obj.slug:
            obj.slug = slugify(obj.name)
            obj.save(update_fields=["slug"])

def noop_reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ("materials", "0006_comment"),
    ]

    operations = [
        migrations.RunPython(create_core_categories, noop_reverse),
    ]
