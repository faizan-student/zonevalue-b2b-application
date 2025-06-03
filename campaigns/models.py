from django.db import models


class CampaignEmail(models.Model):
    email = models.EmailField(unique=True)
    content = models.TextField()
    is_sent = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
