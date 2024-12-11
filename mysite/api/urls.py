from django.urls import path
from .views import blog_list, blog_detail, delete_post, blog_create, edit_post
from . import views

urlpatterns = [
    path('', views.blog_list,),  # Blog list
    path('create/', blog_create),  # Create a new post
    path('blogdetail/<str:pk>/', views.blog_detail),  # Blog detail
    path('<str:pk>/edit/', views.edit_post),  # Update a post
    path('delete_post/', views.delete_post),  # For AJAX
    path('<str:pk>/delete/', views.delete_post),  # Delete a post using views.delete_post
    path('like/<str:post_id>/', views.like_post),  # Like a post
]


