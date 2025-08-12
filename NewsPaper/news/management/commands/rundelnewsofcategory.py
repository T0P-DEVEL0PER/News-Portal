from django.core.management.base import BaseCommand, CommandError
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Команда rundelnewsofcategory удаляет новости и статьи в определённой категории.'
    requires_migrations_checks = True

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        answer = input(f'Вы действительно хотите удалить все новости и статьи в категории {options["category"]}? yes/no')

        if answer != 'yes':
            self.stdout.write(self.style.ERROR('В выполнении команды Вам отказано.'))
            return
        try:
            category = Category.objects.get(name=options['category'])
            Post.objects.filter(category=category).delete()
            self.stdout.write(self.style.SUCCESS(f'Все новости и статьи в категории {category.name} были успешно удалены.'))
        except Category.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'Категории {options['category']} не существует.'))