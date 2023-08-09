"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from config import settings
from django.conf.urls.static import static
from blog.views import (
    home_page,
    log_out,
    log_in,
    register,
    post_page,
    user_posts,
    create_post,
    edit_post,
    delete_post,
)


urlpatterns = [
    path("", home_page, name="home_page"),
    path("admin/", admin.site.urls),
    path("logout", log_out, name="logout"),
    path("login", log_in, name="login"),
    path("register", register, name="register"),
    path("post/<slug:page_slug>", post_page, name="post_page"),
    path("<slug:username>/posts", user_posts, name="user_posts"),
    path("create_post", create_post, name="create_post"),
    path("edit_post/<slug:page_slug>", edit_post, name="edit_post"),
    path("delete_post/<slug:page_slug>", delete_post, name="delete_post"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
