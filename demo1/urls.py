from django.urls import path
from . import views
from .views import register, news_feed, create_post, post_list, profile, edit_profile

urlpatterns = [
    path('game_list', views.game_list, name='game_list'),
    path('post/<int:id>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_create, name='post_create'),
    path('register/', register, name='register'),
    path('', news_feed, name='news_feed'),
    path('create-post/', create_post, name='create_post'),
    path('posts/', post_list, name='post_list'),
    path('game-reviews/', views.game_reviews, name='game_reviews'),
    path('add-game-review/', views.add_game_review, name='add_game_review'),
    path('delete-game-review/<int:review_id>/', views.delete_game_review, name='delete_game_review'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Add this line
    path('profile/<str:username>/', views.profile, name='profile'),
    
]
