from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post


class BlogAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            w.attrs.setdefault("class", "input-control")
            if name == "username":
                w.attrs.setdefault("autocomplete", "username")
            elif name == "password":
                w.attrs.setdefault("autocomplete", "current-password")


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            w.attrs.setdefault("class", "input-control")
            if name == "username":
                w.attrs.setdefault("autocomplete", "username")
            elif name == "email":
                w.attrs.setdefault("autocomplete", "email")
            elif "password" in name:
                w.attrs.setdefault("autocomplete", "new-password")


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "content", "image", "category", "tags")
        widgets = {
            "content": forms.Textarea(attrs={"rows": 12}),
            "tags": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs.setdefault("class", "input-control")
        self.fields["content"].widget.attrs.setdefault("class", "input-control")
        self.fields["image"].widget.attrs.setdefault("class", "input-control input-file")
        self.fields["category"].widget.attrs.setdefault("class", "input-control")


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 4, "placeholder": "Izohingiz..."})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["body"].widget.attrs.setdefault("class", "input-control")
