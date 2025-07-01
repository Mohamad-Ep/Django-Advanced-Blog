from django.contrib import admin
from .models import Post,Category
# __________________________________________________________

class PostAdmin(admin.ModelAdmin):
    list_display = ('title','status','created_date','updated_date','author','category')
    list_filter = ('title','category')
    search_fields = ('title',)
    
admin.site.register(Post)
admin.site.register(Category)


# __________________________________________________________
