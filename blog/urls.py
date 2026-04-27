from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("post/yangi/", views.post_create, name="post_create"),
    path("postlarim/", views.my_posts, name="my_posts"),
    path("register/", views.register, name="register"),
    path("login/", views.BlogLoginView.as_view(), name="login"),
    path("logout/", views.BlogLogoutView.as_view(), name="logout"),
]
