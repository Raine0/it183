from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from .models import BlogPost, Like
from .forms import BlogPostForm
from django.contrib.auth.decorators import login_required
from django.apps import apps
from django.contrib import messages
from .forms import UserRegisterForm
from .models import Profile
from django.shortcuts import get_object_or_404
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES) 
        if form.is_valid():
            user = form.save()
            profile = Profile.objects.create(user=user)
            profile.profile_picture = form.cleaned_data.get('profile_picture')
            profile.bio = form.cleaned_data.get('bio')
            profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog_list') 
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def blog_list(request):
    print(f"LOGIN_REDIRECT_URL: {settings.LOGIN_REDIRECT_URL}")
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')

        if content:
            new_post = BlogPost.objects.create(
                content=content,
                author=request.user, 
                image=image,
            )
            return redirect('blog_list')  

    posts = BlogPost.objects.all().order_by('-date_posted') 
    context = {'posts': posts}
    return render(request, 'blog/blog_list.html', context)


@login_required 
def like_post(request, post_id):
    post = get_object_or_404(BlogPost, pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:  # If the like already exists, then unlike
        like.delete()
        liked = False
    else:
        liked = True

    like_count = post.likes.count()

    # Return the updated like count and liked status
    return JsonResponse({'liked': liked, 'like_count': like_count})


def blog_detail(request, id):
    post = get_object_or_404(BlogPost, id=id)  
    context = {'post': post}
    return render(request, 'blog/blog_detail.html', context)


def blog_delete(request, id):
    each_post = BlogPost.objects.get(id=id)
    each_post.delete()
    return HttpResponseRedirect('/posts/')


@login_required # Make sure the user is logged in
def blog_create(request):
    form = BlogPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        blog_post = form.save(commit=False)  # Don't save yet
        blog_post.author = request.user      # Set the author
        blog_post.save()                     # Now save
        return HttpResponseRedirect('/posts/')
    context = {
        "form": form,
        'form_type': 'Create'
    }
    return render(request, "blog/blog_create.html", context)


@login_required
def blog_update(request, id):
    post = get_object_or_404(BlogPost, id=id)
    form = BlogPostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/posts/')
    context = {
        "form": form,
        "form_type": 'Update'
    }
    return render(request, "blog/blog_create.html", context) #using same template


@login_required  # Make sure only logged-in users can access
def profile(request):
    # You can add more logic here to display user-specific data
    return render(request, 'registration/profile.html')


@login_required
def delete_post(request):
  if request.method == 'POST':
    post_id = request.POST.get('post_id')
    post = get_object_or_404(BlogPost, id=post_id, author=request.user)
    post.delete()
    return JsonResponse({'success': True})


@login_required
def edit_post(request, id):
    post = get_object_or_404(BlogPost, id=id)

    # Handle form data submission
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog_detail', id=post.id)  # Redirect after successfully saving the post
    else:
        form = BlogPostForm(instance=post)  # Pre-populate the form with the existing post data
    
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})