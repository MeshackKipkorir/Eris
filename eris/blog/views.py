from django.shortcuts import render,get_object_or_404
from .models import Post,Category,Comment
from .forms import CommentForm

def index(request,category):
    posts = Post.objects.all()
    categories = Category.objects.all()
    
    if category:
        posts = posts.filter(category = category)
    
    context = {
        "posts":posts,
        "categories":categories
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
    context = {
        "post":post,
        "comments":comments,
        "form":form,
        "comments_count":comments_count
    }
    return render(request,'blog/blog-single.html',context)