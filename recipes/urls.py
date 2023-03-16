from django.urls import path

from . import views

# o ponto abaixo significa : da pasta onde eu estou importe views


# from recipes.views import home


urlpatterns = [
    path('', views.home),
    # <id> é uma variável para indicar o valor que será inserido no caminho da
    # url para identificar cada receita individualmente
    # bem como é um parametro recebido pela função recipe
    # int: -- só aceita inteiros
    path('recipes/<int:id>/', views.recipe),
]
