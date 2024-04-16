from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

class Game(models.Model):
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=50)
    release_date = models.DateField()
    rating = models.IntegerField(default=0)
    review = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    CATEGORY_CHOICES = [
        ('Review', 'Review'),
        ('News', 'News'),
        ('Clip', 'Clip'),
        ('Screenshot', 'Screenshot'),
        ('Message', 'Message'),  # Added to categorize text-based posts
    ]
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True, null=True)  # Now optional, for messages
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts/images/', null=True, blank=True)  # For pictures
    video = models.FileField(upload_to='posts/videos/', null=True, blank=True)  # For videos

    def __str__(self):
        return self.title
    
    
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Like(models.Model):
    post = models.ForeignKey(Post, related_name='likes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class GameReview(models.Model):
    game_name = models.CharField(max_length=100, default='Unknown Game')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.CharField(max_length=50, default='Not Specified')  # Default value added
    platform = models.CharField(max_length=50, default='Not Specified')  # Assuming you might need this too
    hours_played = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rating = models.IntegerField(default=0, choices=[(i, i) for i in range(1, 11)])
    review = models.TextField()
    thumbs_up = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review of {self.game_name} by {self.user.username}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# Create or update a user profile automatically when a user is created or saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()