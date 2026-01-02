from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, TagSerializer, CategorySerializer
from blogs.models import Post, Category, Tag


# POSTS
# TODO:fix add image issue


class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"


# CATEGORIES
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"


# TAGS
class TagList(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TagDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "id"
