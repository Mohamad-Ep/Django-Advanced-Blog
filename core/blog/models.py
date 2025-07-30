from django.db import models
from datetime import datetime
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# __________________________________________________________


class Post(models.Model):
    """
    This is a class difine posts for blog app
    """

    title = models.CharField(max_length=50, verbose_name="عنوان مقاله")
    status = models.BooleanField(default=False, verbose_name="فعال/غیرفعال")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="تاریخ ویرایش")
    published_date = models.DateTimeField(
        default=datetime.now, verbose_name="تاریخ انتشار"
    )
    image = models.ImageField(null=True, blank=True, verbose_name="عکس مقاله")

    author = models.ForeignKey(
        "accounts.Profile",
        verbose_name="نویسنده",
        on_delete=models.CASCADE,
        related_name="blogs",
    )
    category = models.ForeignKey(
        "Category",
        verbose_name="دسته بندی",
        on_delete=models.CASCADE,
        related_name="blogs",
    )

    def __str__(self):
        return self.title

    def get_absolute_api_url(self):
        return reverse("blog:api-v1:post_details", kwargs={"pk": self.pk})

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقاله ها"


# __________________________________________________________


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name=_("نام دسته بندی"))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته مقاله"
        verbose_name_plural = "دسته های مقاله"


# __________________________________________________________
