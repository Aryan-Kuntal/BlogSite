from rest_framework import serializers
from news_blog.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','content','date','user']
        read_only_fields = ['id','date','user']

