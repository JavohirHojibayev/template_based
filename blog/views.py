from datetime import timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import TemplateView

from .forms import BlogAuthenticationForm, CommentForm, PostForm, RegisterForm
from .models import Post


def _approved_posts():
    return (
        Post.objects.filter(is_approved=True)
        .select_related("author", "category")
        .prefetch_related("tags")
    )


def _can_view_post(user, post):
    if post.is_approved:
        return True
    if user.is_staff:
        return True
    if user.is_authenticated and post.author_id == user.id:
        return True
    return False


class HomeView(TemplateView):
    template_name = "blog/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        now = timezone.now()
        week_ago = now - timedelta(days=7)
        month_ago = now - timedelta(days=30)
        base = _approved_posts()
        ctx["latest"] = base[:10]
        ctx["most_viewed"] = base.order_by("-view_count", "-created_at")[:10]
        ctx["week_popular"] = (
            base.filter(created_at__gte=week_ago)
            .order_by("-view_count", "-created_at")[:10]
        )
        ctx["month_popular"] = (
            base.filter(created_at__gte=month_ago)
            .order_by("-view_count", "-created_at")[:10]
        )
        ctx["recommended"] = base.filter(recommended=True).order_by(
            "-created_at"
        )[:10]
        return ctx


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related("author", "category").prefetch_related(
            "tags", "comments__author"
        ),
        slug=slug,
    )
    if not _can_view_post(request.user, post):
        raise Http404()

    session_key = f"viewed_post_{post.pk}"
    if not request.session.get(session_key):
        Post.objects.filter(pk=post.pk).update(view_count=F("view_count") + 1)
        request.session[session_key] = True
        post.refresh_from_db(fields=["view_count"])

    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.warning(
                request, "Izoh qoldirish uchun tizimga kiring yoki ro‘yxatdan o‘ting."
            )
            return redirect("blog:login")

        form = CommentForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.post = post
            c.author = request.user
            c.save()
            messages.success(request, "Izohingiz saqlandi.")
            return redirect(post.get_absolute_url())
    else:
        form = CommentForm()

    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "form": form, "comments": post.comments.all()},
    )


@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.is_approved = False
            post.save()
            form.save_m2m()
            messages.success(
                request,
                "Post yuborildi. Admin tasdig‘idan keyin barcha foydalanuvchilarga ko‘rinadi.",
            )
            return redirect("blog:my_posts")
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {"form": form})


@login_required
def my_posts(request):
    posts = (
        Post.objects.filter(author=request.user)
        .select_related("category")
        .prefetch_related("tags")
        .order_by("-created_at")
    )
    return render(request, "blog/my_posts.html", {"posts": posts})


def register(request):
    if request.user.is_authenticated:
        return redirect("blog:home")
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(
                request,
                "Tabriklaymiz! Ro‘yxatdan muvaffaqiyatli o‘tdingiz — akkaunt yaratildi va siz avtomatik ravishda tizimga kirdingiz.",
            )
            return redirect("blog:home")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


class BlogLoginView(LoginView):
    template_name = "registration/login.html"
    authentication_form = BlogAuthenticationForm


class BlogLogoutView(LogoutView):
    next_page = "/"
