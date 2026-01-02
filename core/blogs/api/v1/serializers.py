from rest_framework import serializers
from blogs.models import Category, Tag, Post
from rest_framework.parsers import MultiPartParser, FormParser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ["id", "name"]


class PostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(), many=True)
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "published_at",
            "updated_at",
            "category",
            "tags",
            "image",
        ]

    def create(self, validated_data):
        category = validated_data.pop("category")
        tags = validated_data.pop("tags")
        post = Post.objects.create(category=category, **validated_data)
        post.tags.set(tags)
        return post
