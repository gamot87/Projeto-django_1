from django.urls import path

from . import views

# o ponto abaixo significa : da pasta onde eu estou importe views


# from recipes.views import home

# o codigo abaixo inicia a variavel name abaixo recipes:recipe
app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    # <id> é uma variável para indicar o valor que será inserido no caminho da
    # url para identificar cada receita individualmente
    # bem como é um parametro recebido pela função recipe
    # int: -- só aceita inteiros
    path('recipes/search/', views.search, name='search'),  # lambda é temporario para que a url exista e passe no teste # noqa : E501
    path('recipes/category/<int:category_id>/',
         views.category, name='category'),
    path('recipes/<int:id>/', views.recipe, name='recipe'),


]
