# from django.http import HttpResponse

from django.shortcuts import get_list_or_404, get_object_or_404, render

# abaixo estamos importando a função que salva os dados no banco de dados
from .models import Recipe

# from utils.recipes.factory import make_recipe


# Create your views here.


def home(request):
    # Abaixo estamos criando uma variavel com o comando sheel que
    # vai relacionar todas as receitas em ordem decrescente
    # ou seja quanto mais recente primeiro sera relacionada
    # recipes = Recipe.objects.filter(
    # is_published=True
    # ).order_by('-id')
    # home.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates

    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')

    return render(request, 'recipes/pages/home.html',
                  context={'recipes': recipes,
                           })


def category(request, category_id):

    # recipes = Recipe.objects.filter(
    #    category__id=category_id,
    #    is_published=True
    # ).order_by('-id')

    # category_name = getattr(getattr(recipes.first(), 'category', None),
    #                       'name',
    #                        'Not found'
    #                        ) 'title': f'{category_name}
    # como eh uma query usamos 'title': f'{recipes.first().category.name} - Category | # noqa:E501
    # if not recipes:
    # raise Http404('Not Found')

    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id'))
    # filtrando
    # como é uma lista usamos o indice
    # 'title': f'{recipes[0].category.name} - Category | '

    return render(request, 'recipes/pages/category.html',
                  context={'recipes': recipes,
                           'title': f'{recipes[0].category.name} - Category | '
                           })


def recipe(request, id):

    # get_object_or_404 é uma atalho que ja informa quando a pagina nao existir
    recipe = get_object_or_404(Recipe,
                               pk=id,
                               is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html',
                  context={'recipe': recipe,
                           'is_detail_page': True
                           })
