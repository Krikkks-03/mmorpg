from django.db import models
from django.conf import settings
from ads.models import Ad

class Response(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='responses')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='responses')
    created_at = models.DateTimeField(auto_now_add=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f'Отклик на {self.ad.title} от {self.author.email}'