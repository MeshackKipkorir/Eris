from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

class LatestPostsFeed(Feed):
    title = 'Eris Blog'
    link = reverse_lazy('blog:index')
    description = 'New posts alert'

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return truncatewords(item.body,40)