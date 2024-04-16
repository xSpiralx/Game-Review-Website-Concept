from django import forms
from .models import Post, GameReview, Profile
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'category', 'image', 'video']  # Ensure this matches your updated model
        widgets = {
            'body': forms.Textarea(attrs={'placeholder': 'Write your message here...'}),
        }


class GameReviewForm(forms.ModelForm):
    class Meta:
        model = GameReview
        fields = ['game_name', 'genre', 'platform', 'hours_played', 'rating', 'review', 'thumbs_up']
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}))

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError('A user with that email already exists.')
        return email

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself...'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control-file'}),
        }
        help_texts = {
            'profile_picture': 'Ideal image size is 256x256px.',
        }