from django.contrib import admin

from .models import Category, Comment, Post, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "author",
        "category",
        "is_approved",
        "recommended",
        "view_count",
        "created_at",
    )
    list_display_links = ("title",)
    list_editable = ("is_approved", "recommended")
    list_filter = ("is_approved", "recommended", "category", "created_at")
    search_fields = ("title", "content", "author__username")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags",)
    readonly_fields = ("view_count", "created_at", "updated_at")
    inlines = [CommentInline]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "title",
                    "slug",
                    "content",
                    "image",
                    "category",
                    "tags",
                    "author",
                )
            },
        ),
        (
            "Moderatsiya",
            {"fields": ("is_approved", "recommended", "view_count")},
        ),
        ("Vaqt", {"fields": ("created_at", "updated_at")}),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "created_at")
    search_fields = ("body", "author__username", "post__title")
    list_filter = ("created_at",)
