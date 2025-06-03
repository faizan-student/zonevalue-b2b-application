from django.urls import path
from .views import (
    EmailCampaignView,
    WhatsAppTemplateSendView,
    redirect_root_to_campaign,
)

urlpatterns = [
    path("send-campaign/", EmailCampaignView.as_view(), name="send_campaign"),
    path("send-whatsapp/", WhatsAppTemplateSendView.as_view(), name="send_whatsapp"),
]
