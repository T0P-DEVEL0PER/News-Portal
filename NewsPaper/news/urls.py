from django.urls import path
from .views import (
    PostsList, PostDetail, NewsCreate, NewsUpdate, NewsDelete,
    ArticlesCreate, ArticlesUpdate, ArticlesDelete, post_search, upgrade_me, LkView,
    TechList, SociumList, CultureList, ScienceList,
    tech_subscribe, socium_subscribe, culture_subscribe, science_subscribe,
)

urlpatterns = [
    path('', PostsList.as_view(), name='posts_list'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('search/', post_search, name="post_search"),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/update/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('articles/create/', ArticlesCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/update/', ArticlesUpdate.as_view(), name='articles_update'),
    path('articles/<int:pk>/delete/', ArticlesDelete.as_view(), name='articles_delete'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('lk/', LkView.as_view(), name='lk'),
    path('tech/', TechList.as_view(), name='tech'),
    path('socium/', SociumList.as_view(), name='socium'),
    path('culture/', CultureList.as_view(), name='culture'),
    path('science/', ScienceList.as_view(), name='science'),
    path('tech_subscribe/', tech_subscribe, name='tech_subscribe'),
    path('socium_subscribe/', socium_subscribe, name='socium_subscribe'),
    path('culture_subscribe/', culture_subscribe, name='culture_subscribe'),
    path('science_subscribe/', science_subscribe, name='science_subscribe'),
]