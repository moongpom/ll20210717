from django import forms
from .models import Post
from .models import Comment
# Create your models here.
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields =['title','hideName','body','image']

class CommentForm(forms.ModelForm):
    body = forms.CharField(label='', max_length=1000, 
        widget=forms.Textarea(attrs={'rows':'3', 'cols': '50'}))
    class Meta:
        model = Comment
        fields =['body','hideName']


class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='Search Word')

