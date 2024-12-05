from django import forms
from .models import Post, Author

class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(queryset=Author.objects.all(), required=True)
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories', 'author', 'post_type'] 