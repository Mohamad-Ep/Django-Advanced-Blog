from django.urls import path, include
from .views import (
    indexView,
    IndexView,
    RedirectDarsman,
    PostList,
    PostDetailsView,
    PostCreateViewByForm,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    PostListApi,
)
from django.views.generic import TemplateView, RedirectView

# __________________________________________________________

app_name = "blog"

urlpatterns = [
    path("index-fbv/", indexView, name="fbv-index"),
    path("index-cbv/", IndexView.as_view(), name="cbv-index"),
    path("", TemplateView.as_view(template_name="blog/index.html"), name="index"),
    path(
        "go-to-digikala/",
        RedirectView.as_view(url="https://digikala.com/"),
        name="go-to-digikala",
    ),
    path("go-to-darsman/", RedirectDarsman.as_view(), name="go-to-darsman"),
    path(
        "go-to-index/",
        RedirectView.as_view(pattern_name="blog:cbv-index"),
        name="go-to-index",
    ),
    path("posts/", PostList.as_view(), name="posts"),
    path("post_details/<int:pk>/", PostDetailsView.as_view(), name="post_details"),
    path("post/createbyform/", PostCreateViewByForm.as_view(), name="post_create_form"),
    path("post/create/", PostCreateView.as_view(), name="post_create"),
    path("post/update/<int:pk>/", PostUpdateView.as_view(), name="post_update"),
    path("post/delete/<int:pk>/", PostDeleteView.as_view(), name="post_delete"),
    path("posts/api/", PostListApi.as_view(), name="api-posts"),    # get api by jquery
    # api-v1
    path("api/v1/", include("blog.api.v1.urls", namespace="api-v1"), name="api-v1"),
]

# __________________________________________________________
