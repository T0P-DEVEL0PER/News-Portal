from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment, UserCategory


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    list_filter = ('user', 'rating')
    search_fields = ('user', 'rating')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_filter = ('name', )
    search_fields = ('name', )


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'article_or_news', 'datetime_of_creation', 'name', 'text', 'rating'
    )
    list_filter = (
        'author', 'article_or_news', 'datetime_of_creation', 'name', 'text', 'rating'
    )
    search_fields = (
        'author', 'article_or_news', 'datetime_of_creation', 'name', 'text', 'rating'
    )


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('post', 'category')
    search_fields = ('post', 'category')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text', 'datetime_of_creation', 'rating')
    list_filter = ('post', 'user', 'text', 'datetime_of_creation', 'rating')
    search_fields = ('post', 'user', 'text', 'datetime_of_creation', 'rating')


class UserCategoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    list_filter = ('user', 'category')
    search_fields = ('user', 'category')


admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(UserCategory, UserCategoryAdmin)