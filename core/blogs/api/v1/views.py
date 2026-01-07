from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PostSerializer, TagSerializer, CategorySerializer
from blogs.models import Post, Category, Tag
from rest_framework.parsers import MultiPartParser, FormParser
from core.utils import IsAdminOrReadOnly
from rest_framework.permissions import IsAdminUser
from core.utils import CustomAnonRateThrottle, CustomUserRateThrottle
from drf_yasg.utils import swagger_auto_schema


# POSTS
class PostList(ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    parser_classes = (MultiPartParser, FormParser)
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Posts"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Posts"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class PostDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminOrReadOnly,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Posts"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Posts"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Posts"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Posts"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# CATEGORIES
class CategoryList(ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Categories"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Categories"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CategoryDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminUser,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Categories"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Categories"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Categories"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Categories"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)


# TAGS
class TagList(ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Tags"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Tags"])
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class TagDetail(RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = "id"
    permission_classes = [
        IsAdminUser,
    ]
    throttle_classes = [CustomUserRateThrottle, CustomAnonRateThrottle]

    @swagger_auto_schema(tags=["Blog-Tags"])
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Tags"])
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Tags"])
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(tags=["Blog-Tags"])
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
