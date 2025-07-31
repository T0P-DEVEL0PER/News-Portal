from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        self.rating = 0.0
        for i in Post.objects.filter(author=self).values("rating"):
            self.rating += i['rating'] * 3
        for i in Comment.objects.filter(user=self.user).values("rating"):
            self.rating += i['rating']
        for i in Comment.objects.filter(post__author=self).values("rating"):
            self.rating += i['rating']
        self.save()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return self.name


class Post(models.Model):
    article = 'AR'
    news = 'NE'

    VARIANTS = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article_or_news = models.CharField(max_length=2, choices=VARIANTS)
    datetime_of_creation = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    name = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'

    def __str__(self):
        return f'{self.name}: {self.text[:20]}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.category.__str__()} - {self.post.__str__()}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    datetime_of_creation = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return self.text[:20]


class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.__str__()} - {self.category.__str__()}'
