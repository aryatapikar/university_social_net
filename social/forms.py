from django import forms
from django.core.exceptions import ValidationError

class PostForm(forms.Form):
    caption = forms.CharField(max_length=200, required=False)
    photo = forms.ImageField(required=False)
    def clean(self):
        cleaned_data = super().clean()
        caption = cleaned_data.get('caption')
        photo = cleaned_data.get('photo')

        if not caption and not photo:
            raise ValidationError('At least one of Caption or Photo must be provided.')

class CommentForm(forms.Form):
    post_id = forms.IntegerField(widget=forms.HiddenInput())
    comment = forms.CharField(widget=forms.Textarea(attrs={'style': 'width: 490px;'}))