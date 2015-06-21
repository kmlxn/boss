from django import forms


class CommentForm(forms.Form):
    comment_text = forms.CharField(label="Comment's text", widget=forms.Textarea)
    comment_image = forms.FileField(required=False)


class AddTopicForm(forms.Form):
    topic_name = forms.CharField(label="Topic's name", max_length=255)
    topic_text = forms.CharField(label="Topic's text", widget=forms.Textarea)
    topic_description = forms.CharField(label="Topic's description", widget=forms.Textarea)
    topic_category = forms.CharField(label="Topic's category", max_length=255)
    image = forms.FileField(required=False)


class AddCategoryForm(forms.Form):
    category_name = forms.CharField(label="Category name", max_length=255)
    category_title = forms.CharField(label="Category title", max_length=255)