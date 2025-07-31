from django.conf import settings
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, send_mail
from .models import PostCategory


@receiver(m2m_changed, sender=PostCategory)
def send_mail_to_subscribers(instance, **kwargs):
    for category in instance.category.all():
        for user in category.subscribers.all():
            send_mail(
                subject=instance.name,
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[user.email],
                html_message=f"""
                    <h1>Здравствуй, {user.username}. Новая статья в твоём любимом разделе!</h1>
                    <h2>{instance.name}</h2>
                    <p>{instance.text[:50]}</p>
                    <button><a href="http://127.0.0.1:8000/news/{instance.pk}">Перейти и прочитать</a></button>
                """,
            )
