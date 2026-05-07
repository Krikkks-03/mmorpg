from django.contrib import admin
from .models import Response

@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ('ad', 'author', 'is_accepted', 'created_at')
    list_filter = ('is_accepted', 'created_at')