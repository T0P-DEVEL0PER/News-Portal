from datetime import date, timedelta
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView,  TemplateView
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from .forms import PostForm
from .models import Post, Author, UserCategory, Category
from .filters import PostFilter


class LkView(LoginRequiredMixin, TemplateView):
    template_name = 'lk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostsList(ListView):
    model = Post
    ordering = '-datetime_of_creation'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        return context


def post_search(request):
    f = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'post_search.html', {'filter': f})


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'NE'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_of_authors_posts'] = len(Post.objects.filter(
            author__user=self.request.user,
            datetime_of_creation__gte=date.today(),
            datetime_of_creation__lt=date.today() + timedelta(days=1)
        ))
        return context


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'news_update.html'


class NewsDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'news_delete.html'
    success_url = reverse_lazy('post_list')


class ArticlesCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post', )
    form_class = PostForm
    model = Post
    template_name = 'articles_create.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.article_or_news = 'AR'
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count_of_authors_posts'] = len(Post.objects.filter(
            author__user=self.request.user,
            datetime_of_creation__gte=date.today(),
            datetime_of_creation__lt=date.today() + timedelta(days=1)
        ))
        return context


class ArticlesUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post', )
    form_class = PostForm
    model = Post
    template_name = 'articles_update.html'


class ArticlesDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'articles_delete.html'
    success_url = reverse_lazy('post_list')


@login_required
def upgrade_me(request):
    user = request.user
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(user)
        Author.objects.create(user=user)
    return redirect('/')

class TechList(ListView):
    model = Post
    ordering = '-datetime_of_creation'
    template_name = 'tech.html'
    context_object_name = 'tech'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['tech'] = Post.objects.filter(category__name='Технологии')
        return context


class SociumList(ListView):
    model = Post
    ordering = '-datetime_of_creation'
    template_name = 'socium.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['socium'] = Post.objects.filter(category__name='Общество')
        return context


class CultureList(ListView):
    model = Post
    ordering = '-datetime_of_creation'
    template_name = 'culture.html'
    context_object_name = 'culture'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['culture'] = Post.objects.filter(category__name='Культура')
        return context


class ScienceList(ListView):
    model = Post
    ordering = '-datetime_of_creation'
    template_name = 'science.html'
    context_object_name = 'science'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_authors'] = not self.request.user.groups.filter(name='authors').exists()
        context['science'] = Post.objects.filter(category__name='Наука')
        return context


@login_required
def tech_subscribe(request):
    UserCategory.objects.create(user=request.user, category=Category.objects.get(name='Технологии'))
    return redirect('http://127.0.0.1:8000/news/tech/')


@login_required
def socium_subscribe(request):
    UserCategory.objects.create(user=request.user, category=Category.objects.get(name='Общество'))
    return redirect('http://127.0.0.1:8000/news/socium/')


@login_required
def culture_subscribe(request):
    UserCategory.objects.create(user=request.user, category=Category.objects.get(name='Культура'))
    return redirect('http://127.0.0.1:8000/news/culture/')


@login_required
def science_subscribe(request):
    UserCategory.objects.create(user=request.user, category=Category.objects.get(name='Наука'))
    return redirect('http://127.0.0.1:8000/news/science/')
