from django.contrib import admin
from .models import Newsletter
from django.core.mail import send_mass_mail
from accounts.models import User

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('subject', 'created_at', 'sent')
    list_filter = ('sent',)
    actions = ['send_newsletter']

    def send_newsletter(self, request, queryset):
        for newsletter in queryset.filter(sent=False):
            emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
            if emails:
                messages = [(newsletter.subject, newsletter.body, None, [email]) for email in emails]
                send_mass_mail(messages, fail_silently=False)
                newsletter.sent = True
                newsletter.save()
            self.message_user(request, f'Рассылка "{newsletter.subject}" отправлена {len(emails)} пользователям')
    send_newsletter.short_description = 'Отправить выбранные рассылки'