from django import forms
from .models import BlogPost, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model  # Import get_user_model

User = get_user_model() # Assign it to User

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['content', 'image']  # Include image field

class UserRegisterForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)  # Add for profile picture

    class Meta(UserCreationForm.Meta):
        model = User  # Use the User variable
        fields = UserCreationForm.Meta.fields + ('profile_picture',)
