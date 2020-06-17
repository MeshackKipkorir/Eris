from django.db import models
from django.utils import timezone 
from django.contrib.auth.models import User 
from django.urls import reverse 
from taggit.managers import TaggableManager

class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,self).get_queryset().filter(status='published')


class Category(models.Model):
    name = models.CharField(max_length = 20)

    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft','Draft'),
        ('published','Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 250,unique_for_date='publish')
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='blog_posts')
    body =  models.TextField()
    category = models.ManyToManyField('Category',related_name='posts')
    publish = models.DateTimeField(default=timezone.now)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail',
        args = [self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug])
    
class Comment(models.Model):
    author = models.CharField(max_length = 60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)
    email = models.EmailField(null = True)
    post = models.ForeignKey('Post',on_delete = models.CASCADE)
    