from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "CEJAM - Centro Educacional Jamilza Moreira"
admin.site.site_title = "CEJAM Admin"
admin.site.index_title = "Administracao"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v2/", include(("apps.api.urls", "api"), namespace="v2")),
    path("api/", include("apps.api.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
