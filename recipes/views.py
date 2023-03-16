# from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.


def home(request):
    # home.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates
    return render(request, 'recipes/pages/home.html', context={'name': 'Gabriel'})


def recipe(request, id):
    # recipe.html = arquivo html que o django a
    # utomaticamente irá procurar na pasta templates
    return render(request, 'recipes/pages/recipe-view.html', context={'name': 'Gabriel'})
