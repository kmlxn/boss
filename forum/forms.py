from django import forms
from captcha.fields import CaptchaField


class CommentForm(forms.Form):
    comment_text = forms.CharField(label="Comment's text", widget=forms.Textarea(
        attrs={"id": "comment_text", "placeholder": "comment text"}
    ))
    comment_image = forms.FileField(required=False)
    comment_captcha = CaptchaField()


class AddTopicForm(forms.Form):
    topic_name = forms.CharField(label="Topic's name", max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Name", "id": "topic_name"}
        )
    )
    topic_text = forms.CharField(label="Topic's text",
        widget=forms.Textarea(
            attrs={"rows": "3", "id": "topic_text"}
        )
    )
    topic_description = forms.CharField(label="Topic's description",
        widget=forms.Textarea(
            attrs={"id": "topic_description"}
        )
    )
    topic_category = forms.CharField(label="Topic's category", max_length=255,
        widget=forms.TextInput(
            attrs={"id": "topic_category"}
        )
    )
    topic_image = forms.FileField(required=False)
    topic_captcha = CaptchaField()


class AddCategoryForm(forms.Form):
    category_name = forms.CharField(label="Category name", max_length=255)
    category_title = forms.CharField(label="Category title", max_length=255)

class UploadImageForm(forms.Form):
    image = forms.FileField()
