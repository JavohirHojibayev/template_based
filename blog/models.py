from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField("nom", max_length=120)
    slug = models.SlugField(unique=True, max_length=140, blank=True)

    class Meta:
        verbose_name = "bo‘lim"
        verbose_name_plural = "bo‘limlar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or "category"
        super().save(*args, **kwargs)


class Tag(models.Model):
    name = models.CharField("teg", max_length=80)
    slug = models.SlugField(unique=True, max_length=100, blank=True)

    class Meta:
        verbose_name = "teg"
        verbose_name_plural = "teglar"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name) or "tag"
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField("sarlavha", max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    content = models.TextField("matn")
    image = models.ImageField("rasm", upload_to="posts/%Y/%m/")
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="posts",
        verbose_name="bo‘lim",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="teglar")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_posts",
    )
    is_approved = models.BooleanField("admin tasdig‘i", default=False)
    recommended = models.BooleanField("tavsiya qilingan", default=False)
    view_count = models.PositiveIntegerField("ko‘rishlar soni", default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "post"
        verbose_name_plural = "postlar"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title) or "post"
            slug = base
            n = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{n}"
                n += 1
            self.slug = slug
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="blog_comments",
    )
    body = models.TextField("izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = "izoh"
        verbose_name_plural = "izohlar"

    def __str__(self):
        return f"{self.author}: {self.body[:40]}"
