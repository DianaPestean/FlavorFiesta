from django.forms import ModelForm
from django import forms
from .models import Recipe

class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'featured_image',
            'description',              #ADD COOKING TIME HERE
            'ingredients',
            'steps',
            'tags',
        ]
        widgets = {
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
