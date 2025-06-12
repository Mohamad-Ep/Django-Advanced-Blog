from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User,Profile
# __________________________________________________________

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email','created_date','updated_date','is_active','is_staff','is_superuser')
    ordering = ('created_date',)
    search_fields = ('email',)
    
    fieldsets = (
        (_('Authentication'), {"fields": ("email", "password")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": ("email", "usable_password", "password1", "password2"),
            },
        ),
    )
    
admin.site.register(User,CustomUserAdmin)
# __________________________________________________________

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','first_name','last_name','created_date')
    
admin.site.register(Profile)
# __________________________________________________________