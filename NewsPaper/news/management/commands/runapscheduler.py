from datetime import datetime, timedelta
import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives, send_mail
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.template.loader import render_to_string
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from news.models import Category, Post

logger = logging.getLogger(__name__)


def my_job():
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
                """,
            )


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/604800"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info(
            "Added weekly job: 'delete_old_job_executions'."
        )

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
