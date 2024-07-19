from rest_framework import serializers

from .models import Comment, Post


class PostReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def get_likes(self, obj):
        likes = list(
            like.username for like in obj.likes.get_queryset().only("username")
        )
        return likes

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['total_likes'] = instance.likes.count()
        return data

class PostWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = "__all__"

class CommentReadSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"

class CommentWriteSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = "__all__"
