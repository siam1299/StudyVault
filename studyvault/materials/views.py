# materials/views.py
from django.http import FileResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MaterialForm
from django.core.paginator import Paginator
from .models import Material, University
from django.http import JsonResponse
from .models import Material, Upvote
from .models import Downvote
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string
from .forms import CommentForm
from .models import Comment
from django.db.models import F
import mimetypes, os



@login_required
def upload_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.uploader = request.user
            material.save()
            messages.success(request, "Material uploaded successfully!")
            return redirect("materials:upload")
    else:
        form = MaterialForm()

    return render(request, "materials/upload.html", {"form": form})

def browse_materials(request):
    qs = Material.objects.all().select_related("category", "department", "semester", "uploader")

    # Search
    q = request.GET.get("q")
    if q:
        qs = qs.filter(title__icontains=q) | qs.filter(description__icontains=q)

    # Filter by category/department/semester
    category = request.GET.get("category")
    if category:
        qs = qs.filter(category__id=category)

    department = request.GET.get("department")
    if department:
        qs = qs.filter(department__id=department)

    semester = request.GET.get("semester")
    if semester:
        qs = qs.filter(semester__id=semester)

    # ✅ NEW: university filter
    university = request.GET.get("university")
    if university:
        qs = qs.filter(university__id=university)

    # Pagination
    paginator = Paginator(qs, 10)  # প্রতি পেইজে ১০টা ফাইল
    page = request.GET.get("page")
    materials = paginator.get_page(page)

    context = {
        "materials": materials,
    }
    return render(request, "materials/browse.html", context)

def universities_list(request):
    universities = University.objects.all().order_by("name")
    return render(request, "materials/universities.html", {"universities": universities})

def material_detail(request, pk):
    material = get_object_or_404(Material, pk=pk)

    # ফাইল এক্সটেনশন বের করা
    file_url = material.file.url.lower()
    if file_url.endswith((".jpg", ".jpeg", ".png")):
        file_type = "image"
    elif file_url.endswith(".pdf"):
        file_type = "pdf"
    else:
        file_type = "other"

    return render(request, "materials/detail.html", {
        "material": material,
        "file_type": file_type,
    })

@require_POST
@login_required
def toggle_upvote(request, pk):
    material = get_object_or_404(Material, pk=pk)

    existing = Upvote.objects.filter(user=request.user, material=material)
    if existing.exists():
        existing.delete()
        your_vote = "none"
    else:
        Downvote.objects.filter(user=request.user, material=material).delete()
        Upvote.objects.create(user=request.user, material=material)
        your_vote = "up"

    return JsonResponse({
        "status": "ok",
        "your_vote": your_vote,
        "total_upvotes": material.upvotes.count(),
        "total_downvotes": material.downvotes.count(),
    })

@login_required
@require_POST
def toggle_downvote(request, pk):
    material = get_object_or_404(Material, pk=pk)

    existing = Downvote.objects.filter(user=request.user, material=material)
    if existing.exists():
        existing.delete()
        your_vote = "none"
    else:
        Upvote.objects.filter(user=request.user, material=material).delete()
        Downvote.objects.create(user=request.user, material=material)
        your_vote = "down"

    return JsonResponse({
        "status": "ok",
        "your_vote": your_vote,
        "total_upvotes": material.upvotes.count(),
        "total_downvotes": material.downvotes.count(),
    })


@login_required
@require_POST
def add_comment(request, pk):
    material = get_object_or_404(Material, pk=pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        c = form.save(commit=False)
        c.material = material
        c.user = request.user
        c.save()
        html = render_to_string("materials/_comment.html", {"c": c}, request=request)
        return JsonResponse({"ok": True, "html": html, "count": material.comments.count()})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def add_reply(request, pk):
    """
    AJAX reply handler.
    Expect: body, parent_id  (x-www-form-urlencoded)
    """
    material = get_object_or_404(Material, pk=pk)

    body = (request.POST.get("body") or "").strip()
    parent_id = request.POST.get("parent_id")

    if not body:
        return JsonResponse({"ok": False, "errors": {"body": ["This field is required."]}}, status=400)
    if not parent_id:
        return JsonResponse({"ok": False, "errors": {"parent_id": ["Missing parent_id."]}}, status=400)

    parent = get_object_or_404(Comment, pk=parent_id, material=material)

    c = Comment.objects.create(
        material=material,
        user=request.user,
        body=body,
        parent=parent,
    )

    html = render_to_string("materials/_comment.html", {"c": c}, request=request)
    return JsonResponse({"ok": True, "html": html})


@login_required
@require_POST
def delete_comment(request, comment_id):
    """
    Delete a comment (owner or staff only). Returns JSON.
    """
    c = get_object_or_404(Comment, pk=comment_id)

    if (c.user_id != request.user.id) and (not request.user.is_staff):
        return JsonResponse({"ok": False, "error": "forbidden"}, status=403)

    cid = c.id
    c.delete()
    return JsonResponse({"ok": True, "comment_id": cid})


def download_file(request, pk):
    material = get_object_or_404(Material, pk=pk)
    file_path = material.file.path  # ধরে নিচ্ছি field নাম file

    if not os.path.exists(file_path):
        raise Http404("File not found")

    # ✅ Download count increase
    material.download_count = F('download_count') + 1
    material.save(update_fields=['download_count'])
    material.refresh_from_db(fields=['download_count'])  # আপডেট রিফ্রেশ

    # ✅ File response তৈরি
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
    return response
