from django.contrib import admin

from .models import (
    Ingredient,
    IngredientInRecipe,
    FavoriteRecipe,
    RecipeList,
    ShoppingCart,
    Tag
)


class RecipeIngredientsAdmin(admin.StackedInline):
    model = IngredientInRecipe
    autocomplete_fields = ('ingredient',)


@admin.register(RecipeList)
class RecipeListAdmin(admin.ModelAdmin):
    inlines = (RecipeIngredientsAdmin,)
    list_display = ('author', 'name', 'text')
    search_fields = (
        'name', 'cooking_time',
        'author__username', 'ingredients__name'
    )
    list_filter = (
        'pub_date', 'tags',
    )
    empty_value_display = '-пусто-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'color', 'slug',)
    search_fields = ('name', 'slug',)
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'measurement_unit',)
    search_fields = (
        'name', 'measurement_unit',)
    empty_value_display = '-пусто-'


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    ordering = ('user',)
    search_fields = ('recipe', 'user')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    ordering = ('user',)
    search_fields = ('recipe', 'user')
    empty_value_display = '-пусто-'
