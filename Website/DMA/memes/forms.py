from django import forms
from .models import Post, Comment, Reply
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            "text",
        ]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = [
            "text",
        ]