# Apesar de ter o mesmo nome da classe que importamos do django.test
# essa classe importada do unittes éum pouco mais simples nos asserts
from unittest import TestCase

from django.urls import reverse

# queremos que os numeros das paginas fiquem como no google, exemplo: 1 2 3 4 e a pagina que estamos em azul, e que ela avance para 5  # noqa:E501
# quando a pagina atual for 3 e assim m por diante até a pagina 20 , onde na pagina 19 e 20 deve-se obter 17,18,19,20 pois nosso range é de 20  # noqa:E501
# paginas entao nao é possivel avançar, enfimfrom recipes import views, vamos testar essa logica  # noqa:E501
from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    # testando se a função retorna o nosso range de paginas
    def test_make_pagination_range_returns_a_pagination_range(self):
        # current page = 1 - qty page =2 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([1, 2, 3, 4], pagination)
    # testando se a exibição das duas primeiras paginas está estatica

    def test_first_range_is_static_of_current_page_is_less_than_middle_page(self):  # noqa:E501
        # current page = 1 - qty page =2 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([1, 2, 3, 4], pagination)
        # current page = 2 - qty page =2 - middle page = 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )
    # abaixo testamos se a partir da 3 pagina a lista de paginas muda progressivamente(dinamicamente) # noqa:E501

    def test_make_sure_middle_ranges_are_correct(self):  # noqa:E501

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([2, 3, 4, 5], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=5,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([4, 5, 6, 7], pagination)

    # abaixo testamos se a logica está correta para as utimas 2 paginas onde a exibição deverá ser estatica [17,18,19,20]# noqa:E501
    def test_make_sure_final_ranges_are_correct(self):  # noqa:E501

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([17, 18, 19, 20], pagination)

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([17, 18, 19, 20], pagination)

    def test_page_is_bigger_than_max_pagination_limit(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=22,
        )['pagination']  # <- aki colocamos para ele buscar a chave de pagination do dicionario que é retornado da função make_pagination_range # noqa:E501
        self.assertEqual([17, 18, 19, 20], pagination)


class PaginationTests(RecipeTestBase):
    # Vamos testar se estão sendo exibidas o numero correto de receitas por página image.png # noqa:E501
    def test_pagination_max_9_recipes_por_page(self):
        list_recipes = []
        # looping para criar varias receitas, no caso 16
        for x in range(0, 15):
            x = self.make_recipe(title=f'recipe0{str(x)}', slug=str(
                x), author_data={'username': f'{str(x)}'})
            list_recipes.append(x.title)
        # variavel com o total de receitas criado
        total_recipes_created = len(list_recipes)
        # Variavel com a resposta da view
        response = self.client.get(reverse('recipes:home'))

        # variavel com o total de receitas exibidas na pagina página
        total_recipes_showed_in_the_page = len(
            response.context['recipes'].object_list)
        # Vamos primeiro verificar se o número de receitas criados é maior que o numero de receitas que deve ser exibido # noqa:E501
        # assim podemos ter certeza que temos mais de uma página de receitas.
        # Codigo comentado abaixo serve para fazer o teste falhar.
        # self.assertGreater(total_recipes_created, 20)
        self.assertGreater(total_recipes_created, 9)
        # Abaixo verificamos se o número de receitas exibidos tem o máximo de 9 por página # noqa:E501
        # Para testar o código abaixo basta ir na view home e alterar o valor de PER_PAGES para mais ou para menos de 9 em make_pagination # noqa:E501
        self.assertEqual(total_recipes_showed_in_the_page, 9)

    def test_pagination_less_than_9_recipes_per_page(self):
        # Vamos testar se quando tivermos um numero de receitas menor que o máximo por página(geralmente a ultima página) # noqa:E501
        # o numero correto será exibido
        # looping para criar 4 receitas
        list_recipes = []
        for x in range(0, 4):
            x = self.make_recipe(title=f'recipe0{str(x)}', slug=str(
                x), author_data={'username': f'{str(x)}'})
            list_recipes.append(x.title)
        total_recipes_created = len(list_recipes)
        # Variavel com a resposta da view
        response = self.client.get(reverse('recipes:home'))
        # variavel com o total de receitas criado
        content = response.content.decode('utf-8')
        # Para fazer falhar o codigo abaixo basta alterar na view home o valor de  PER_PAGES para 4 ou mais # noqa:E501
        self.assertLess(total_recipes_created, 9)
        # Código comentado abaixo para fazer o teste falhar pois sabemos que 'Recipetest' não esta contido no conteudo # noqa:E501
        # list_recipes.append('Recipetest')

        # Abaixo criamos um Looping para verificar se cada receita(valor do titulo) é encontrado no content # noqa:E501
        for recipe in list_recipes:
            self.assertIn(recipe, content)
