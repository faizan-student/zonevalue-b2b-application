from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from campaigns.views import redirect_root_to_campaign


urlpatterns = [
    path("", redirect_root_to_campaign, name="root_redirect"),
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("campaigns/", include("campaigns.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
