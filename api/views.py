from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from news_blog.models import Post
from .serializers import PostSerializer
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
import json
# Create your views here.

@api_view(["GET",'POST'])
@permission_classes([IsAdminUser])
def get_blogs(request):
    if request.method == 'GET':
        posts = Post.objects.all()

        serializer = PostSerializer(posts,many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = PostSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAdminUser])
def make_changes(request,id):
    try:
        post = Post.objects.get(id=id)
    except Post.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


    if request.method == 'DELETE':
        post.delete()
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    if request.method == 'PUT':
        data = json.loads(request.body)
        post = Post.objects.filter(id=id)
        post.update(title=data['title'],content=data['content'])
        serializer = PostSerializer(post[0])
        return Response(serializer.data,status=status.HTTP_202_ACCEPTED)