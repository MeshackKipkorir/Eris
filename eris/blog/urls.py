from django.urls import path 
from . import views
from .feeds import LatestPostsFeed
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('',views.index,name="index"),
    path('tag/<slug:tag_slug>/',views.index,name='post_list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_detail,name="post_detail"),
    path('<int:post_id>/share/',views.post_share,name='share_post'),
    path('feed/',LatestPostsFeed(), name = 'post_feed'),
    path('register/',views.registerUser,name = 'register'),
    path('login/',views.user_login,name = 'login'),
    path('edit/',views.edit,name='edit_profile'),
    path('add/',views.add_blog,name='add_blog'),
]