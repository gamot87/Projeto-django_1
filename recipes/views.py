# from django.http import HttpResponse
from django.shortcuts import render

from utils.recipes.factory import make_recipe

# abaixo estamos importando a função que salva os dados no banco de dados
from .models import Recipe

# Create your views here.


def home(request):
    # Abaixo estamos criando uma variavel com o comando sheel que
    # vai relacionar todas as receitas em ordem decrescente
    # ou seja quanto mais recente primeiro sera relacionada
    recipes = Recipe.objects.filter(
        is_published=True
    ).order_by('-id')
    # home.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates
    return render(request, 'recipes/pages/home.html',
                  context={'recipes': recipes,
                           })


def category(request, category_id):

    recipes = Recipe.objects.filter(
        category__id=category_id,
        is_published=True
    ).order_by('-id')

    return render(request, 'recipes/pages/category.html',
                  context={'recipes': recipes,
                           })


def recipe(request, id):
    # recipe.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates
    return render(request, 'recipes/pages/recipe-view.html',
                  context={'recipe': make_recipe(),
                           'is_detail_page': True
                           })
