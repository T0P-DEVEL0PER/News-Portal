from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import send_mail
from .models import Post, Category


@shared_task
def mail_to_subs(instance_pk):
    instance = Post.objects.get(pk=instance_pk)
    for category in instance.category.all():
        for user in category.subscribers.all():
            send_mail(
                subject=instance.name,
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[user.email],
                html_message=f"""
                    <h1>Здравствуй, {user.username}. Еще не прочитал(а) новую статью? Если нет, то нужно это сделать как можно скорее!</h1>
                    <h2>{instance.name}</h2>
                    <p>{instance.text[:50]}</p>
                    <button><a href="http://127.0.0.1:8000/news/{instance.pk}">Перейти и прочитать</a></button>
                    <p>При отправке этого письма были использованы технологии, предоставляемые Redis и Celery.</p>
                """,
            )


@shared_task
def news_of_week():
    for category in Category.objects.all():
        for user in category.subscribers.all():
            messages = []
            posts = Post.objects.filter(category=category, datetime_of_creation__gt=datetime.now() - timedelta(days=7))
            for post in posts:
                message = f"""
                    <h2>{post.name}</h2>
                    <p>{post.text[:50]}</p>
                    <button><a href="http://127.0.0.1:8000/news/{post.pk}">Перейти и прочитать</a></button>
                """,
                messages.append(''.join(message))
            send_mail(
                subject=f'Список новостей и статей в категории {category.name} за последнюю неделю.',
                message='',
                from_email='igreatprojectsi@yandex.ru',
                recipient_list=[user.email],
                html_message=f"""
                    <h1>Здравствуй, {user.username}. Список новостей и статей в категории {category.name} за последнюю неделю!</h1>
                    {', '.join(messages)}
                    <p>При отправке этого письма были использованы технологии, предоставляемые Redis и Celery.</p>
                """,
            )
