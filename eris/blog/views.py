from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Category,Comment,Profile
from .forms import CommentForm,EmailShareForm,LoginForm,UserRegistrationForm,ProfileEditForm,AddBlogForm
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count
from django.contrib.auth import authenticate,login
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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
    form = UserRegistrationForm()
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit = False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,'registration/register_done.html',{'new_user':new_user})
        
        else:
            form = UserRegistrationForm()
            
    return render(request,'registration/register.html',{'form':form})


def user_login(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        user = authenticate(request,username = cd['username'],password = cd['password'])
        
        if user is not None:
            if user.is_active:
                login(request,user)
                return redirect('/')

            else: 
                return  HttpResponse('Account has been disabled')
        
        else:
            return HttpResponse('Invalid Login attempt')

    return render(request,'registration/login.html',{'form':form})


@login_required
def edit(request):
    profile_form = ProfileEditForm()

    if request.method == 'POST':
        profile_form = ProfileEditForm(instance = request.user, data = request.POST)

        if profile_form.is_valid():
            profile_form.save()

    else:
        profile_form = ProfileEditForm()
    return render(request,'blog/edit.html',{'profile_form':profile_form})

@login_required
def add_blog(request):
    message = ""
    form = AddBlogForm()
    if request.method == "POST":
        form = AddBlogForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            form = AddBlogForm()
            return redirect('index')
            
    else:
        form = AddBlogForm()
    

    return render(request,'blog/add-blog.html',{'form':form,'message':message})