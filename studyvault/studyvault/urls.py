from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, profile_view   # ✅ profile_view ইমপোর্ট করো

urlpatterns = [
    path('', home, name='home'),
    path('u/<str:username>/', profile_view, name='profile'),  # ✅ নতুন লাইন
    path('admin/', admin.site.urls),

    # তোমার কাস্টম accounts (login, signup, logout)
    path('accounts/', include('accounts.urls')),

    # allauth (Google login সহ)
    path('accounts/', include('allauth.urls')),

    # ✅ materials
    path('materials/', include('materials.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)