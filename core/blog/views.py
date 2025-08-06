from django.shortcuts import render, redirect
from django.views.generic import (
    TemplateView,
    RedirectView,
    ListView,
    DetailView,
    FormView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Post
from django.contrib import messages
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# from django.contrib.auth.decorators import permission_required

# __________________________________________________________


# @permission_required("blog.view_post")
def indexView(request):
    """
    function for load index page
    """
    context = {"name": "Ali", "age": 25}
    return render(request, "blog/index.html", context)


# __________________________________________________________


class IndexView(TemplateView):
    """
    class for load Index page

    """

    template_name = "blog/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["name"] = "Hasan"
        context["family"] = "Asar"
        return context


# __________________________________________________________


class RedirectDarsman(RedirectView):
    """
    This class for test RedirectView to Darsman.com
    """

    url = "https://darsman.com"


# __________________________________________________________

"""
Permission for object to permission_required ↓

blog.delete_post        # داخل اپ بلاگ دسترسی دیلیت پست را داشته باشد
blog.change_post
blog.view_post
blog.add_post

"""


class PostList(PermissionRequiredMixin, ListView):
    # model = Post
    permission_required = (
        "blog.view_post",
        "blog.add_post",
    )  # or permission_required = 'blog.change_post'
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    queryset = Post.objects.filter(status=True)
    ordering = "-published_date"
    paginate_by = 4

    # def get_queryset(self):
    #     posts = Post.objects.filter(status=True)
    #     return posts


# __________________________________________________________


class PostDetailsView(DetailView):
    model = Post
    context_object_name = "post"
    template_name = "blog/post_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Blog Detail"
        return context


# __________________________________________________________


class PostCreateViewByForm(LoginRequiredMixin, FormView):
    template_name = "blog/post_create_form.html"
    form_class = PostForm
    success_url = "/blog/posts/"

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


# __________________________________________________________


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = "blog/post_form.html"
    model = Post
    fields = ["title", "status", "category"]
    success_url = "/blog/posts/"

    def form_valid(self, form):
        form.instance.author = (
            self.request.user
        )  # برای زمانی که میخواهیم نویسنده رو بصورت اتوماتیک اون یوزری که لاگین هست قرار دهیم
        return super().form_valid(form)


# __________________________________________________________


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    success_url = "/blog/posts/"


# __________________________________________________________


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = "/blog/posts/"


# __________________________________________________________
