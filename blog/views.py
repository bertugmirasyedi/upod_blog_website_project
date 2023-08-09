from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import BlogPost


def home_page(request):
    headline_posts = list(
        BlogPost.objects.filter(is_deleted=False).order_by("-created_at")
    )[:3]

    all_posts = BlogPost.objects.filter(is_deleted=False).order_by("-created_at")

    context = {
        "title": "blog.",
        "user": request.user,
        "headline_posts": headline_posts,
        "posts": all_posts,
    }

    return render(request, "home.html", context)


def post_page(request, page_slug):
    post = BlogPost.objects.filter(slug=page_slug)[0]

    context = {"post": post, "title": post.title}

    return render(request, "post_page.html", context)


@login_required(login_url="login")
def user_posts(request, username):
    user = User.objects.filter(username=username)[0]

    user_posts = BlogPost.objects.filter(user=user, is_deleted=False).order_by(
        "-created_at"
    )

    context = {"posts": user_posts}

    return render(request, "user_posts.html", context)


@login_required(login_url="login")
def create_post(request):
    if request.method == "POST":
        user = User.objects.filter(username=request.user.username)[0]
        post_title = request.POST.get("post_title")
        post_content = request.POST.get("post_content")
        post_image = request.FILES.get("post_image")

        BlogPost.objects.create(
            user=user,
            title=post_title,
            body=post_content,
            image=post_image,
        )

        messages.success(request, "Post oluşturuldu.")

        return redirect("user_posts", username=user.username)

    context = {"title": "blog. - Yeni Gönderi Oluştur"}

    return render(request, "create_post.html", context)


@login_required(login_url="login")
def edit_post(request, page_slug):
    post = BlogPost.objects.filter(slug=page_slug)[0]

    if request.user.username == post.user.username:
        if request.method == "POST":
            post_title = (
                post.title
                if request.POST.get("post_title") == ""
                else request.POST.get("post_title")
            )
            post_content = (
                post.body
                if request.POST.get("post_content") == ""
                else request.POST.get("post_content")
            )
            post_image = (
                post.image
                if request.FILES.get("post_image") == ""
                else request.FILES.get("post_image")
            )

            post.title = post_title
            post.body = post_content
            post.image = post_image

            post.save(update_slug=True)

            messages.success(request, "Gönderi düzenlendi.")

            return redirect("user_posts", username=post.user.username)
    else:
        messages.warning(request, "Bu gönderiyi düzenleme yetkiniz yok.")

        return redirect("home_page")

    context = {"title": "blog. - Gönderi Düzenle", "post": post}

    return render(request, "edit_post.html", context)


@login_required(login_url="login")
def delete_post(request, page_slug):
    post = BlogPost.objects.filter(slug=page_slug)[0]

    if request.user.username == post.user.username:
        post.is_deleted = True

        post.save()

        messages.success(request, "Gönderi silindi.")

        return redirect("user_posts", username=post.user.username)

    else:
        messages.warning(request, "Bu gönderiyi silme yetkiniz yok.")

        return redirect("home_page")


def log_in(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        messages.success(request, "Giriş başarılı.")
        login(request, user)
    else:
        messages.warning(request, "Kullanıcı adı veya şifre hatalı.")

    return redirect("home_page")


def register(request):
    username = request.POST.get("username")
    password = request.POST.get("password")
    password_confirm = request.POST.get("password_confirm")

    if password != password_confirm:
        messages.warning(request, "Şifreler uyuşmuyor.")
        return redirect("home_page")

    if User.objects.filter(username=username).exists():
        messages.warning(request, "Bu kullanıcı adı zaten kayıtlı.")
        return redirect("home_page")

    user = authenticate(request, username=username, password=password)

    if user is not None:
        messages.info(request, "Bu kullanıcı bilgileri zaten kayıtlı. Giriş yapılıyor.")
        login(request, user)
    else:
        user = User.objects.create_user(username=username, password=password)
        user.save()
        messages.success(
            request, f"{user.username} adlı kullanıcı oluşturuldu. Giriş yapılıyor."
        )
        login(request, user)

    return redirect("home_page")


def log_out(request):
    messages.success(request, "Çıkış yapıldı.")
    logout(request)

    return redirect("home_page")
