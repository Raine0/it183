from django.contrib import admin
from .models import BlogPost, Like  # Import your Like model

admin.site.register(BlogPost)  # If you haven't already registered BlogPost
admin.site.register(Like)
