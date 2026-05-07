from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='ads')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('ad_detail', args=[str(self.id)])