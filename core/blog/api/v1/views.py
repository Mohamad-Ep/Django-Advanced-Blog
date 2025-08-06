from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, APIView, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework import status
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import CustomPagination
from django_filters import rest_framework as filters

# __________________________________________________________


@api_view()
def index_api(request):
    return Response({"data": "Hello"})


# __________________________________________________________

# function Besed View for api


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([permissions.IsAuthenticated])
def post_details(request, id):
    if request.method == "GET":
        post = get_object_or_404(Post, id=id)
        ser_data = PostSerializer(instance=post)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        post = get_object_or_404(Post, id=id)
        ser_data = PostSerializer(instance=post, data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
    elif request.method == "DELETE":
        post = get_object_or_404(Post, id=id)
        post.delete()
        return Response(
            {"details": "Object Delete is Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# __________________________________________________________


@api_view(["GET", "POST"])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        ser_data = PostSerializer(instance=posts, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        ser_data = PostSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================================

# class Besed View for api


class PostList(APIView):
    """getting & Creating postList"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        """getting post-list"""
        posts = Post.objects.filter(status=True)
        ser_data = PostSerializer(instance=posts, many=True)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """creating post"""
        ser_data = PostSerializer(data=request.data)
        if ser_data.is_valid():
            ser_data.save()
            return Response(data=ser_data.data, status=status.HTTP_200_OK)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


# __________________________________________________________


class PostDetails(APIView):
    """getting single post & put & delete that"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        """getting single post"""
        post = get_object_or_404(Post, id=self.kwargs["id"])
        ser_data = PostSerializer(instance=post)
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        """editing single post"""
        post = get_object_or_404(Post, id=self.kwargs["id"])
        ser_data = PostSerializer(instance=post, data=request.data)
        ser_data.is_valid(raise_exception=True)
        ser_data.save()
        return Response(data=ser_data.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        """deleting single post"""
        post = get_object_or_404(Post, id=self.kwargs["id"])
        post.delete()
        return Response(
            {"details": "Object Delete is Successfully"},
            status=status.HTTP_204_NO_CONTENT,
        )


# ============================================================

# Generic Api View By Classes


class PostListByGeneric(ListCreateAPIView):
    """getting & Creating postList by generics"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)


# __________________________________________________________


class PostDetailsByGeneric(RetrieveUpdateDestroyAPIView):
    """getting single post & put & delete that by generics"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    lookup_field = "id"


# ============================================================

# ViewSet Api

# class PostViewSet(viewsets.ViewSet):
#     """ CRUD operation by ViewSet """
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = PostSerializer
#     queryset = Post.objects.filter(status=True)

#     def list(self, request):
#         ser_data = self.serializer_class(self.queryset,many=True)
#         return Response(ser_data.data,status=status.HTTP_200_OK)

#     def create(self, request):
#         ser_data = self.serializer_class(data=request.data)
#         ser_data.is_valid(raise_exception=True)
#         ser_data.save()
#         return Response(data=ser_data.data,status=status.HTTP_201_CREATED)

#     def retrieve(self, request, pk=None):
#         post = get_object_or_404(self.queryset,pk=pk)
#         ser_data = self.serializer_class(post)
#         return Response(data=ser_data.data,status=status.HTTP_200_OK)

#     def update(self, request, pk=None):
#         post = get_object_or_404(self.queryset,pk=pk)
#         ser_data = self.serializer_class(post,data=request.data)
#         ser_data.is_valid(raise_exception=True)
#         ser_data.save()
#         return Response(data=ser_data.data,status=status.HTTP_200_OK)

#     def partial_update(self, request, pk=None):
#         post = get_object_or_404(self.queryset,pk=pk)
#         ser_data = self.serializer_class(post,data=request.data,partial=True)
#         ser_data.is_valid(raise_exception=True)
#         ser_data.save()
#         return Response(data=ser_data.data,status=status.HTTP_200_OK)

#     def destroy(self, request, pk=None):
#         post = get_object_or_404(self.queryset,pk=pk)
#         post.delete()
#         return Response(data={'details':'object is deleted'},status=status.HTTP_204_NO_CONTENT)

# --------------------------------------

# class PostCustomFilter(filters.filterset):
#     published_date_gte = filters.NumberFilter(field_name='published_date',lookup_expr='year__gte')
#     published_date_lte = filters.NumberFilter(field_name='published_date',lookup_expr='year__lte')

#     class Meta:
#         model = Post
#         fields = ['category','author']


class PostViewSet(viewsets.ModelViewSet):
    """CRUD operation by ViewSet"""

    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = ['category', 'author']
    filterset_fields = {
        "category": ["exact", "in"],
        "author": ["exact"],
    }  # در حالت اگزکت میشه خودش و درحالت این میشه چندتا کتگوری رو باهم فیلتر کرد
    # filterset_class = PostCustomFilter
    search_fields = ["title", "author__first_name", "category__name"]
    ordering_fields = ["published_date"]
    pagination_class = CustomPagination


# __________________________________________________________


class CategoryModelViewSet(viewsets.ModelViewSet):
    """CRUD operation by ModelViewSet"""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    @action(methods=["get"], detail=False)
    def get_simple(self, reuqest):
        return Response({"details": "This is simple Text"})

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)


# __________________________________________________________
