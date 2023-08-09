from django.db import models
from django.contrib.auth.models import User
from slugify import slugify


class BlogPost(models.Model):
    title = models.CharField(max_length=150)
    body = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    slug = models.SlugField(max_length=150, unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    image = models.ImageField(
        upload_to="images/",
        blank=True,
        null=True,
        default="images/blog_post_img.jpg",
    )

    def save(self, *args, update_slug=False, **kwargs):
        if not self.slug or update_slug:
            self.slug = slugify(self.title, allow_unicode=False)

        super().save(*args, **kwargs)

    def get_short_body(self, n=70):
        return f"{self.body[:n]}..."

    def get_mid_body(self, n=300):
        return f"{self.body[:n]}..."

    def __str__(self):
        return self.title
