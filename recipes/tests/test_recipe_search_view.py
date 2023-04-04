from unittest import skip  # noqa: F401

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# @skip('Pular testes abaixo')
# Importamos as views
# Create your tests here.
# RecipeViewsTest está herdando de RecipeTestBase(do arquivo test_recipe_base) os metodos(e todos os metodos de TestCase) e ainda sim é um objeto TestCase # noqa:E501
class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_uses_correct_view_function(self):
        resolved = resolve(reverse('recipes:search'))
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        # o teste abaixo quebrou esse teste pois a view estava subindo o erro 404 caso o valor colocado fosse vazio # noqa:E501
        # então para que o teste volte  funcionar adicionamos a url o valor de um imput('?q=teste') # noqa:E501
        # assim ele renderiza o template apontado na view
        url = reverse('recipes:search') + '?q=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search_term(self):
        # url = reverse('recipes:search') + '?q=teste' ->>> para testar basta colocar essa variavel url no lugar de # noqa:E501
        # 'recipes:search' pois o valor seria 200 e ai nao passaria
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    # O Teste abaixo é muito importante pois ele identifica se nossos caracteres em determinada local da pagina # noqa:E501
    # no caso um input esta Escaped, se sim podemos ficar tranquilos em relação a segurança pois nenhum script # noqa:E501
    # malicioso vai denificar nossa aplicação, caso contrário temos que corrigir # noqa:E501
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        # O que é ESCAPED HTML? HTML permite que caracteres especiais sejam representados por sequências de escape, indicadas por # noqa:E501
        # três partes: um & inicial, um número ou cadeia de caracteres correspondente ao caracter desejado, e um ; final. Como vemos, # noqa:E501
        # as sequências de escape são sensíveis à caixa.
        url = reverse('recipes:search') + '?q=Teste'
        response = self.client.get(url)

        self.assertIn(
            # usamos &quot;Teste&quot; pq "=&quot em html e assim ele pode identificar para descobrir qual codigo usar # noqa:E501
            # é só esperar falhar o teste e pesquisar na pagina de erro pela string que queremos testar (no nosso caso Teste) # noqa:E501
            # e entao ela aparecerá com o codigo referente ao caracterer usado # noqa:E501
            'Search for &quot;Teste&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'this is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'},
        )

        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'},
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        # verifica se as variaveis de recipe 1 batem com a resposta da sua receita # noqa:E501
        self.assertIn(recipe1, response1.context['recipes'])
        # verifica se as variaveis sao diferentes no contexto de outra receita
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
