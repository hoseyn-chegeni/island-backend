from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, TagSerializer, CategorySerializer
from blogs.models import Post, Category, Tag
from rest_framework.parsers import MultiPartParser, FormParser
from core.utils import IsOwnerOrAdmin, IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser

# POSTS
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser)


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"
    permission_classes = [IsAdminOrReadOnly,]


# CATEGORIES
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    permission_classes = [IsAdminUser,]

# TAGS
class TagList(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()


class TagDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "id"
    permission_classes = [IsAdminUser,]