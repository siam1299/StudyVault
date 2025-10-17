# materials/urls.py
from django.urls import path
from . import views

app_name = "materials"

urlpatterns = [
    path("upload/", views.upload_material, name="upload"),
    path("browse/", views.browse_materials, name="browse"),
    path("universities/", views.universities_list, name="universities"),
    path("<int:pk>/", views.material_detail, name="material_detail"),

    path("<int:pk>/upvote/", views.toggle_upvote, name="toggle_upvote"),
    path("<int:pk>/downvote/", views.toggle_downvote, name="toggle_downvote"),
    # comments
    path("<int:pk>/comment/", views.add_comment, name="add_comment"),

    # materials/urls.py
    path("<int:pk>/reply/", views.add_reply, name="add_reply"),

    path("comment/<int:comment_id>/delete/", views.delete_comment, name="delete_comment"),

]
