from django import template 
from ..models import Post

register = template.Library()

@register.inclusion_tag('blog/latest_posts.html')
def latest_posts(count = 5):
    #retribe latest posts ordered by date published, count variabke limits number of posts
    latest_posts = Post.objects.order_by('-publish')[:count]
    return {'latest_posts':latest_posts}