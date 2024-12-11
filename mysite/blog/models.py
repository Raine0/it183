from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from PIL import Image # Import Pillow
from django.conf import settings



class BlogPost(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
  

    def __str__(self):
        return self.content

    # Optional: Resize image after upload (keep original)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs) 
        if self.image:
            img = Image.open(self.image.path) 
            if img.height > 300 or img.width > 300: # check size
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')  # Ensure a user can only like a post once

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


from .models import BlogPost # Import the BlogPost model


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
