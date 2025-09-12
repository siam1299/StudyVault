from django.contrib import admin
from django.urls import path, include
from .views import home   # এটাও ঠিক আছে, বদলাতে হবে না
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
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