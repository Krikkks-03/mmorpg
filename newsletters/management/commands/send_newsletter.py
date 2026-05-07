from django.core.management.base import BaseCommand
from django.core.mail import send_mass_mail
from django.conf import settings
from newsletters.models import Newsletter
from accounts.models import User

class Command(BaseCommand):
    help = 'Send unsent newsletters'

    def handle(self, *args, **options):
        for newsletter in Newsletter.objects.filter(sent=False):
            emails = list(User.objects.filter(is_active=True).values_list('email', flat=True))
            if not emails:
                self.stdout.write('No active users.')
                continue
            messages = []
            for email in emails:
                messages.append((
                    newsletter.subject,
                    newsletter.body,
                    settings.DEFAULT_FROM_EMAIL,
                    [email]
                ))
            send_mass_mail(messages, fail_silently=False)
            newsletter.sent = True
            newsletter.save()
            self.stdout.write(self.style.SUCCESS(f'Newsletter "{newsletter.subject}" sent to {len(emails)} users'))