from django.contrib import admin

from .models import Category, Recipe

# Register your models here

# Criamos os models mas temos que registralos


class CategoryAdmin(admin.ModelAdmin):
    ...

# Com o codigo abaixo a tabela abaixo (Recipe) é cadastrada por aqui mesmo


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    ...


admin.site.register(Category, CategoryAdmin)
