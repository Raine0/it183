from django.urls import path
from .views import blog_list, blog_detail, blog_delete, blog_create, blog_update, edit_post, delete_post, like_post
from . import views

urlpatterns = [
    path('', views.blog_list, name='blog_list'),  # Blog list
    path('create/', blog_create, name='blog_create'),  # Create a new post
    path('<int:id>/', views.blog_detail, name='blog_detail'),  # Blog detail
    path('<int:id>/edit/', views.edit_post, name='edit_post'),  # Update a post
    path('delete_post/', views.delete_post, name='delete_post_ajax'),  # For AJAX
    path('<int:id>/delete/', views.delete_post, name='delete_post'),  # Delete a post using views.delete_post
    path('like/<int:post_id>/', views.like_post, name='like_post'),  # Like a post
]


