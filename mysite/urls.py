from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static
from django.conf import settings

from django.contrib.sitemaps.views import sitemap
from app.sitemaps import ItemSitemap

# sitemapの設定
sitemaps = {
    'items': ItemSitemap,
}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("app.urls")),
    path("accounts/", include("accounts.urls")),
    path("accounts/", include("allauth.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
