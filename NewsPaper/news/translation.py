from .models import Post, Category
from modeltranslation.translator import register, TranslationOptions


@register(Post)
class PostTranslationOptions(TranslationOptions):
    fields = ('datetime_of_creation', 'name', 'text')


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)
