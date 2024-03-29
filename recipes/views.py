# from django.http import HttpResponse

# modulo de paginação do django
# from django.core.paginator import Paginator
# Para indicar o django que queremos OR ao inves de AND
import os  # Para permitir o uso de variaveis de ambiente

# importa um modulo que permite enviar mensagens ao usuario atraves das views # noqa:E501
from django.contrib import messages  # noqa:F401
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render

from utils.pagination import make_pagination

# abaixo estamos importando a função que salva os dados no banco de dados
from .models import Recipe

# from utils.recipes.factory import make_recipe


# Create your views here.
# Pegamos o valor da variavel de ambiente usando o modulo os e utilizando o nome da variavel # noqa:E501
# e se nao tiver nenhum valor usamos 6 como padrão
PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request):

    # Abaixo estamos criando uma variavel com o comando sheel que vai filtrar as receitar de  # noqa:E501
    # acordo com a variavel is_published e listar todas em ordem decrescente ou seja quanto  # noqa:E501
    # mais recente primeiro sera relacionada
    # recipes = Recipe.objects.filter(
    # is_published=True
    # ).order_by('-id')
    # home.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates

    recipes = Recipe.objects.filter(
        is_published=True,
    ).order_by('-id')
    # Codigo abaixo é um exemplo de como enviar mensagens ao usuario
    # messages.success(request, 'Epa você foi pesquisar que eu vi.')
    # messages.error(request, 'Epa você foi pesquisar que eu vi.')
    # messages.info(request, 'Epa você foi pesquisar que eu vi.')

    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)

    return render(request, 'recipes/pages/home.html',
                  context={'recipes': page_obj,
                           'pagination_range': pagination_range,
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
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/category.html',
                  context={'recipes': page_obj,
                           'pagination_range': pagination_range,
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


def search(request):

    # vamos capturar o valor (q) digitado no input do search
    # caso nao tenha valor ele retorna None
    search_term = request.GET.get('q', "").strip()  # .strip remove espaços laterais seja na esquerda ou direita # noqa:E501
    # vamos condicionar para caso o usuario nao digite nada
    # a view faça uma ação
    if not search_term:  # se nao tiver nada em search_term subir um erro 404
        raise Http404()

    # vamos filtrar as receitas onde o titulo tiver o valor pesquisado ou search_term# noqa:E501
    recipes = Recipe.objects.filter(
        # precisamos fazer uma busca por algo que estaja contido no titulo e nao seja exatamente igual# noqa:E501
        # entao a nossa query tem que se basear no conceito de like no sql que siguinica contem# noqa:E501
        # assim sendo adicionamos (__contains) a variavel que queremos para que ele procure se ela esta contida # noqa:E501
        # o i em __icontains é para ignorar letras maiusculas ou minusculas # noqa:E501
        # observa-se que o filtro abaixo nao vai ser muito efetivo ja que buscando no debug(str(recipes.query)), # noqa:E501
        # a query na verdade so encontra receitas onde o search_term estiver em ambas as variavels # noqa:E501
        # ou seja o operador AND, entao importamos o modulo abaixo # noqa:E501
        # from django.db.models import Q # Para indicar o django que queremos OR # noqa:E501
        # e envolvemos as variaveis em Q() e o | significa OR

        Q(title__icontains=search_term) | Q(
            description__icontains=search_term),
        # e para usar o AND basta usar uma virgula para separar os termos
        is_published=True
        ).order_by('-id')  # ordenado do id maior para o menor ou seja , pela logica os ultimos a serem criados vao aparecer primeiro # noqa:E501
    # apos a cada criação adiciona +1 ao maior id que será para o proxima receita # noqa:E501
    page_obj, pagination_range = make_pagination(request, recipes, PER_PAGE)
    return render(request, 'recipes/pages/search.html', {
        # o valor da variavel page_title(no template em pages search.html) recebe essa string # noqa:E501
        #  + o valor do search_term (value do imput na partial search.html)  # noqa:E501
        'page_title': f'Search for "{search_term}" |',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}',
                  })
