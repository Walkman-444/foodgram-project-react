from django.contrib.auth import get_user_model
from django.core import validators
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(
        'Название тега',
        max_length=60,
        unique=True
    )
    color = models.CharField(
        'Цвет в формате HEX',
        max_length=7,
        unique=True
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=80,
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['-id']

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Единица измерения ингредиента',
        max_length=20,
    )

    class Meta:
        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}.'


class RecipeList(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=255
    )
    image = models.ImageField(
        'Ссылка на картинку',
        upload_to='static/recipe/',
        blank=True,
        null=True
    )
    text = models.TextField(
        'Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        related_name='recipe'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг'
    )
    cooking_time = models.PositiveIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[validators.MinValueValidator(
            1, message='Минимальное время приготовления `1` минута!'), ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return f'{self.author.email}, {self.name}'


class IngredientInRecipe(models.Model):
    recipe = models.ForeignKey(
        RecipeList,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        'Ingredient',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient'
    )
    amount = models.PositiveIntegerField(
        default=1,
        validators=(
            validators.MinValueValidator(
                1, message='Минимальное количество ингридиентов `1` !'),),
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'Количество ингредиентов'
        verbose_name_plural = 'Количество ингредиента'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_and_ingredient')
        ]


class RecipeUserList(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(RecipeList, on_delete=models.CASCADE,
                               verbose_name='Рецепт')


    class Meta:
        abstract = True
        ordering = ('user', 'recipe')


class FavoriteRecipe(RecipeUserList):
    class Meta(RecipeUserList.Meta):
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite_list_user'
            )
        ]

    def __str__(self):
        return (f'Пользователь {self.user.username} '
                f'добавил {self.recipe.name} в избранное.')


class ShoppingCart(RecipeUserList):
    class Meta(RecipeUserList.Meta):
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_cart_list_user'
            )
        ]

    def __str__(self):
        return (f'Пользователь {self.user.username} '
                f'добавил {self.recipe.name} в покупки.')
