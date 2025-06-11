from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, PostForm, CommentForm, UserCreationForm
from .models import Profile, Post, Category, Tag, Comment, Like
from django.db.models import Q

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            user = authenticate(username=user.username,password=request.POST['password1'],backend='django.contrib.auth.backends.ModelBackend')
            if user:
                login(request, user)
                return redirect('home')

    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form, 'categories':Category.objects.all(),'tags':Tag.objects.all()})




@login_required
def profile(request, username):
    if request.user.username != username:
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        posts = Post.objects.filter(author__profile__user=user).order_by('-created_at')
    else:
        user = request.user
        profile = get_object_or_404(Profile, user=user)
        posts = Post.objects.filter(author__profile__user=user).order_by('-created_at')
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=username)
    else:
        form = ProfileForm(instance=profile)
    
    is_owner = (request.user.username == username)
    
    return render(request, 'blog/profile.html', {
        'profile': profile,
        'posts': posts,
        'form': form,
        'is_owner': is_owner,
        'editing': False  
    })


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    for post in posts:
        post.comment_count = post.comments.count()
        post.like_count = post.likes.count()
    categories =Category.objects.all()
    tags = Tag.objects.all()
    return render(request, 'blog/home.html',{'posts':posts,'categories':categories,'tags':tags})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()  # Save many-to-many relationships (categories, tags)
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.comment_count = post.comments.count()
    post.like_count = post.likes.count()


    if request.method == "POST":
        form = CommentForm(request.POST,request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    comments= post.comments.all().order_by('-created_at')
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments,'form':form})


def contact(request):
    return render(request, 'blog/contact.html')

def help(request):
    return render(request, 'blog/help.html')

def faq(request):
    return render(request, 'blog/faq.html')

def privacy(request):
    return render(request, 'blog/privacy.html')

def terms(request):
    return render(request, 'blog/terms.html')

def about(request):
    return render(request, 'blog/about.html')

def search(request):
    query = request.GET.get('q')
    posts = Post.objects.none()
    if query:
        posts = Post.objects.filter(
            Q(title__contains=query) |
            Q(content__contains=query) |
            Q(author__username__contains=query)
        ).distinct()
    return render(request, 'blog/search.html', {'posts': posts, 'query': query})

"""@login_required
def logout(request):
    auth_logout(request)
    return redirect('home')"""
    



@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            post.delete()
            return redirect('home')
        return render(request, 'blog/confirm_delete.html', {'post': post})
    return redirect('post_detail', post_id=post_id)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user == post.author:
        if request.method == 'POST':
            form = PostForm(request.POST,request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post_id)
        else:
            form = PostForm(instance=post)
            return render(request, 'blog/edit_post.html',{'form':form, 'post':post})
        return redirect('post_detail', post_id= post_id)
    

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
    else:
        post.likes.add(user)
        post.refresh_from_db()
    return redirect('post_detail',post_id=post_id)

@login_required
def delete_comment(request, post_id, comment_id):
    post =get_object_or_404(Post, id=post_id)
    comment = get_object_or_404(Comment, id=comment_id, post=post)
    if request.user == comment.author:
        if request.method == 'POST':
            comment.delete()
            return redirect('post_detail',post_id=post_id)
        return render(request, 'blog/confirm_delete_comment.html',{'post':post,'comment':comment})
    return redirect('post_detail', post_id=post_id)

@login_required
def edit_comment(request, post_id,comment_id):
    post = get_object_or_404(Post, id = post_id)
    comment =get_object_or_404(Comment, id=comment_id,post=post)
    if request.user == comment.author:
        if request.method =='POST':
            form =CommentForm(request.POST,request.FILES, instance=comment)
            if form.is_valid():
                form.save()
                return redirect('post_detail',post_id=post_id)
        else:
            form = CommentForm(instance=comment)
        return render(request, 'blog/edit_comment.html',{'form':form,'post':post,'comment':comment})
    return redirect('post_detail',post_id=post_id)

@login_required
def like_comment(request, post_id, comment_id):
    post = get_object_or_404(Post,id=post_id)
    comment= get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
        else:
            comment.likes.add(request.user)
    return redirect('post_detail', post_id=post_id)

@login_required
def category_posts(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(categories=category).order_by('-created_at')
    for post in posts:
        post.comment_count = post.comments.count()
        post.like_count = post.likes.count()
    return render(request, 'blog/home.html',{'posts':posts,'categories':Category.objects.all(),'tags':Tag.objects.all()})

@login_required
def tag_posts(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag).order_by('-created_at')
    for post in posts:
        post.comment_count = post.comments.count()
        post.like_count =  post.likes.count()
    return render(request, 'blog/home.html',{'posts':posts,'categories':Category.objects.all(),'tags':Tag.objects.all()})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk =post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(author=request.user,post=post, content=content)
        return redirect('post_detail', post_id=post_id)
    return redirect('home')


@login_required
def hide_comment(request, comment_id):
    comment = get_object_or_404(Comment, pk = comment_id)
    post = comment.post
    if post and post.author == request.user:
        comment.is_hidden = not comment.is_hidden
        comment.save()
        messages.success(request, f'Comment{'hidden' if comment.is_hidden else 'unhidden'} successfully')
    else:
        messages.error(request, 'You do not have permission to hide this comment.')
    return redirect('post_detail', post_id=post.pk)

    
