from django.forms import ModelForm
from django.core.exceptions import ValidationError

from . import models

class PostForm(ModelForm):
    class Meta:
        model = models.Post
        exclude = ("active","author")

    # customize validation
    def clean_post(self):
        min_words = 5

        data = self.cleaned_data["post"]

        if (data.count(" ") + data.count("\n")) < min_words:
            raise ValidationError(f"Post should have more than {min_words} words.")

        return data