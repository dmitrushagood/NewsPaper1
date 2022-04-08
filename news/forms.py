from django.forms import ModelForm, BooleanField
from .models import Post



class PostForm(ModelForm):
    check_box = BooleanField(label='Ало, Галочка!')

    class Meta:
        model = Post
        fields = ['post', 'Post', 'title', 'text', 'check_box']


