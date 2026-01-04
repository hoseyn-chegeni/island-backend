from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, TagSerializer, CategorySerializer
from blogs.models import Post, Category, Tag
from rest_framework.parsers import MultiPartParser, FormParser
from core.utils import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser
from core.utils import CustomAnonRateThrottle, CustomUserRateThrottle


# POSTS
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


# CATEGORIES
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminUser,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


# TAGS
class TagList(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]


class TagDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminUser,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]
