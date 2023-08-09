from django.contrib import admin
from .models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "created_at",
        "updated_at",
        "slug",
    ]

    prepopulated_fields = {"slug": ("title",)}


# Register your models here.
admin.site.register(BlogPost, BlogPostAdmin)
