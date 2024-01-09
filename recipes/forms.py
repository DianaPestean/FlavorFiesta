from django.forms import ModelForm
from django import forms
from .models import Recipe, Review

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'featured_image',
            'description',              
            'ingredients',
            'steps',
            'tags',
        ]
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
            'ingredients':forms.Textarea(attrs={'rows':20}),
            'steps':forms.Textarea(attrs={'rows':20})
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = [
            'value',
            'body',
        ]
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment with your vote',
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
