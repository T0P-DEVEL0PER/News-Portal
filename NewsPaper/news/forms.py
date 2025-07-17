from django import forms
from django.contrib.auth.models import Group
from allauth.account.forms import SignupForm
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['author', 'category', 'name', 'text']


class CommonSignupForm(SignupForm):

    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        basic_group = Group.objects.get(name='common')
        basic_group.user_set.add(user)
        return user
