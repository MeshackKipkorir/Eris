from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Comment
from .forms import CommentForm,EmailShareForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count


def index(request,tag_slug=None):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag,slug = tag_slug)
        posts = posts.filter(tags__in=[tag])
     
    context = {
        "posts":posts,
        "categories":categories,
        "tag":tag
    }
    return render(request,'blog/index.html',context)

def post_detail(request,year,month,day,post):
    post = get_object_or_404(Post, slug = post,status = 'published',publish__year = year, publish__month = month,publish__day = day)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author = form.cleaned_data["author"],
                body = form.cleaned_data["body"],
                post = post
            )  
            comment.save()

    comments = Comment.objects.filter(post = post)
    comments_count = Comment.objects.filter(post = post).all().count()
    
    post_tags_id = post.tags.values_list('id',flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_id)
    similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]

    context = {
        "post":post,
        "comments":comments,
        "form":form,
        "comments_count":comments_count,
        "similar_posts":similar_posts
    }
    return render(request,'blog/blog-single.html',context)

def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    sent = False
    form = EmailShareForm()
    if request.method == 'POST':
        form = EmailShareForm(data = request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{data['name']} recommends you read" f"{post.title}" 
            message = f"Read {post.title} at {post_url}\n\n" f"{data['name']}\'s comments : {data['comment']}"
            send_mail(subject, message,'meshkemz@gmail.com',[data['to']])
            sent = True
    else:
        form = EmailShareForm()
    return render(request,'blog/share.html',{'form':form,'post':post,'sent':sent})

def registerUser(request):

    return render(request,'blog/register.html',{})


def login(request):
    return render(request,'blog/login.html',{})