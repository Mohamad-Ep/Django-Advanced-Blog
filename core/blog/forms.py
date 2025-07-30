from django import forms
from .models import Post

# __________________________________________________________


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=10, required=True, widget=forms.TextInput())

    class Meta:
        model = Post
        fields = ["title", "status", "author", "category"]

    def clean_title(self):
        title = self.cleaned_data["title"]
        if len(title) < 3:
            raise forms.ValidationError("عنوان نباید کمتر از 3 کاراکتر باشد")
        return title


# __________________________________________________________
