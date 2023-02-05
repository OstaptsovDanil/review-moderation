from django import forms
from .models import Feedback


class AddReviewForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['original_text']
        widgets = {
            'original_text': forms.Textarea(attrs={'cols': 80, 'rows': 20})
        }
        labels = {
            'original_text': 'Текст отзыва'
        }

    def clean_original_text(self):
        text = self.cleaned_data['original_text']
        if len(text) < 100:
            self.add_error('original_text', 'должно быть хотя бы 100 символов')
        return text
