from django.shortcuts import render, redirect, get_object_or_404
from .models import Game, GameReview
from .models import Post
from django.conf import settings
from .forms import PostForm, GameReviewForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('news_feed')  # Redirect to the news feed page
    else:
        form = PostForm()
    return render(request, 'demo1/create_post.html', {'form': form})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user  # Set the author of the post to the current user
            post.save()
            return redirect('news_feed')  # Redirect to the news feed page after creating the post
    else:
        form = PostForm()
    return render(request, 'demo1/post_create.html', {'form': form})


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'demo1/game_list.html', {'posts': posts})


def game_list(request):
    games = Game.objects.all()
    return render(request, 'demo1/game_list.html', {'games': games})

def game_detail(request, id):
    game = Game.objects.get(pk=id)
    return render(request, 'library/game_detail.html', {'game': game})

def post_detail(request, id):
    post = Post.objects.get(id=id)
    return render(request, 'demo1/post_detail.html', {'post': post})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('news_feed')  # Use the URL name here, not the template name
    else:
        form = UserCreationForm()
    return render(request, 'demo1/register.html', {'form': form})



def news_feed(request):
    posts = Post.objects.all().order_by('-created_at')  # Fetch all posts ordered by creation date
    return render(request, 'demo1/news_feed.html', {'posts': posts})


def game_reviews(request):
    reviews = GameReview.objects.all().order_by('-created_at')
    return render(request, 'demo1/game_reviews.html', {'reviews': reviews})

@login_required
def add_game_review(request):
    if request.method == 'POST':
        form = GameReviewForm(request.POST)
        if form.is_valid():
            game_review = form.save(commit=False)
            game_review.user = request.user
            game_review.save()
            return redirect('game_reviews')
    else:
        form = GameReviewForm()
    return render(request, 'demo1/add_game_review.html', {'form': form})

@login_required
def delete_game_review(request, review_id):
    review = GameReview.objects.get(id=review_id, user=request.user)
    review.delete()
    return redirect('game_reviews')

def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-created_at')
    context = {
        'user': user,
        'posts': posts,
        'DEFAULT_PROFILE_PICTURE_URL': settings.DEFAULT_PROFILE_PICTURE_URL,
    }
    return render(request, 'demo1/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            return redirect('profile', username=request.user.username)
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {'u_form': u_form, 'p_form': p_form}
    return render(request, 'demo1/edit_profile.html', context)