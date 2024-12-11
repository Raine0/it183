from rest_framework.response import Response
from rest_framework.decorators import api_view
from blog.models import BlogPost
from .serializers import PostSerializer

@api_view(['GET'])
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-date_posted') 
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def blog_detail(request, pk):
    post = BlogPost.objects.get(id=pk)
    serializer = PostSerializer(post, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def blog_create(request):
    serializer = PostSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['POST'])
def edit_post(request, pk):
    post = BlogPost.objects.get(id=pk)
    serializer = PostSerializer(instance=post, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['DELETE'])
def delete_post(request, pk):
    post = BlogPost.objects.get(id=pk)
    post.delete()
    return Response('Post Deleted', status=204)

@api_view(['POST'])
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
    return Response({'liked': liked, 'like_count': like_count}, status=200)
