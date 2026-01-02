from django.urls import path, include
from .v1.views import (
    TagDetail,
    TagList,
    PostDetail,
    PostList,
    CategoryDetail,
    CategoryList,
)



urlpatterns = [
    path("posts/",PostList.as_view()),
    path("posts/<int:id>/",PostDetail.as_view()),

    path("tags/",TagList.as_view()),
    path("tags/<int:id>/",TagDetail.as_view()),

    path("categories/",CategoryList.as_view()),
    path("categories/<int:id>/",CategoryDetail.as_view()),
]
