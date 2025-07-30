from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

# __________________________________________________________

# router = SimpleRouter()   # برای بعضی مواقع که میخواهیم روترهارو تغییر دهیم
router = DefaultRouter()
router.register("posts", views.PostViewSet, basename="posts")
router.register("categories", views.CategoryModelViewSet, basename="categories")


# __________________________________________________________

app_name = "api-v1"

urlpatterns = [
    path("index/", views.index_api, name="index"),
    # path('post/<int:id>/', views.post_details, name='post_details'),
    # path('post/<int:id>/', views.PostDetails.as_view(), name='post_details'),
    # path('post/<int:id>/', views.PostDetailsByGeneric.as_view(), name='post_details'),
    # path('post-list/', views.post_list, name='post-list'),
    # path('post-list/', views.PostList.as_view(), name='post-list'),
    # path('post-list/', views.PostListByGeneric.as_view(), name='post-list'),
    # viewset
    path(
        "post-list/",
        views.PostViewSet.as_view({"get": "list", "post": "create"}),
        name="post-list",
    ),
    path(
        "post/<int:pk>/",
        views.PostViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="post_details",
    ),
] + router.urls

# __________________________________________________________
