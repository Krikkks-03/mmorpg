from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Response

@receiver(post_save, sender=Response)
def send_notification_to_ad_author(sender, instance, created, **kwargs):
    """При создании нового отклика отправляем письмо автору объявления"""
    if created:
        send_mail(
            subject='Новый отклик на ваше объявление',
            message=f'Пользователь {instance.author.email} оставил отклик:\n\n{instance.text[:500]}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[instance.ad.author.email],
            fail_silently=False,
        )

@receiver(pre_save, sender=Response)
def send_notification_on_accept(sender, instance, **kwargs):
    """При изменении отклика (принятие) отправляем письмо автору отклика"""
    if instance.pk:
        old = Response.objects.get(pk=instance.pk)
        # Если статус изменился с False на True
        if not old.is_accepted and instance.is_accepted:
            send_mail(
                subject='Ваш отклик принят!',
                message=f'Автор объявления "{instance.ad.title}" принял ваш отклик.',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[instance.author.email],
                fail_silently=False,
            )