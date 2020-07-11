from django.contrib import admin
from .models import Recipe

class RecipeAdmin(admin.ModelAdmin):
    list_display = ("recipe_name","user", "public")

admin.site.register(Recipe,RecipeAdmin)
#admin.site.register(Good_recipe)
