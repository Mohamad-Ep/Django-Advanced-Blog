from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from .users import User
# __________________________________________________________

class Profile(models.Model):
    
    user = models.ForeignKey("User", verbose_name=_('کاربر'), on_delete=models.CASCADE, related_name='profiles')
    first_name = models.CharField(max_length=50, verbose_name=_('نام'))
    last_name = models.CharField(max_length=100, verbose_name=_('نام خانوادگی'))
    image = models.ImageField(null=True, blank=True, verbose_name=_('عکس'))
    description = models.TextField(verbose_name=_('توضیحات'))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_('تاریخ درج'))
    updated_date = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ ویرایش'))
    
    def __str__(self):
        return self.user.email
    
    class Meta:
        verbose_name = _('پروفایل کاربر')
        verbose_name_plural = _('پروفایل کاربران')
        

"""
Signal for Create Profile after created User ↓
"""
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# __________________________________________________________
