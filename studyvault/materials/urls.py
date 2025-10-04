# materials/urls.py
from django.urls import path
from . import views

app_name = "materials"

urlpatterns = [
    path("upload/", views.upload_material, name="upload"),
    path("browse/", views.browse_materials, name="browse"),
    path("universities/", views.universities_list, name="universities"),  # ✅ নতুন
    path("<int:pk>/", views.material_detail, name="material_detail"),  # ✅ নতুন

    # ✅ নতুন path for upvote
    path("<int:pk>/upvote/", views.toggle_upvote, name="toggle_upvote"),
    # 👇 নতুন (Downvote)
    path("<int:pk>/downvote/", views.toggle_downvote, name="toggle_downvote"),

]
