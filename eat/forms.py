from django import forms
from .models import Recipe

class RecipeForm(forms.ModelForm):

    ingredient = forms.CharField(
        widget=forms.TextInput(attrs={"size":40}),
        max_length=200,
        label="材料"
        )

    class Meta:
        model = Recipe
        exclude = ["user", "good_coount", "good_user", "quote_user", "quote_recipe", "quote"]
