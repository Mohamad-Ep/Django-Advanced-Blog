from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
# __________________________________________________________

class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """
    def create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError(_('the email is required'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_active',True)
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_("Superuser must have is_superuser=True."))
        
        return self.create_user(email, password, **extra_fields )
# __________________________________________________________

class User(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(max_length=128,unique=True,verbose_name=_('ایمیل'))
    created_date = models.DateTimeField(auto_now_add=True,verbose_name=_('تاریخ درج'))
    updated_date = models.DateTimeField(auto_now=True,verbose_name=_('تاریخ ویرایش'))
    is_active = models.BooleanField(default=False,verbose_name=_('فعال/غیرفعال'))
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    # user_verficated = models.BooleanField(verbose_name=_('تاییدشده'))
    
    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

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
Signal for reate Profile after created User ↓
"""
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
# __________________________________________________________
