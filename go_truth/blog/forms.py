from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment, Category, Tag

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'bio', 'contact', 'link', 'profile_picture', 'location']



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'categories', 'tags', 'image', 'video']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the queryset and labels for categories
        self.fields['categories'].queryset = Category.objects.all()
        self.fields['categories'].label_from_instance = lambda obj: obj.name
        # Customize the queryset and labels for tags
        self.fields['tags'].queryset = Tag.objects.all()
        self.fields['tags'].label_from_instance = lambda obj: obj.name

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content','image','video']
