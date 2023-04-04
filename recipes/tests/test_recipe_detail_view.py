from unittest import skip  # noqa: F401

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# @skip('Pular testes abaixo')
# Importamos as views
# Create your tests here.
# RecipeViewsTest está herdando de RecipeTestBase(do arquivo test_recipe_base) os metodos(e todos os metodos de TestCase) e ainda sim é um objeto TestCase # noqa:E501
class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_view_functions_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        # estamos perguntando de view.func é = views.home
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_returns_404_if_no_recipes_found(self):  # noqa:E501
        # client serve para simular um usuario que irá fazer um request na url especificada # noqa:E501
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 10000}))
        # status_code é uma informação que temos na variavel response, ela pode ser verificada fazendo o debug com break point # noqa:E501
        # na linha abaixo e verificar em depurar (3 icone de cima para baixo, apos a lupa) quais propiedades a variavel tem # noqa:E501
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_the_correct_recipe(self):
        # Testa se existe uma pagina de recipe details (detalhes)
        needed_title = 'this is a detail page - it load one recipe'
        # need a recipe for this test
        self.make_recipe(title=needed_title)  # mudamos o title para testar se ele gera um igual # noqa:E501
        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': 1}))
        content = response.content.decode('utf-8')
        # check
        self.assertIn(needed_title,
                      content)

    def test_recipe_detail_template_dont_load_recipe_not_published(self):
        # test if recipe is_published = False dont show
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.id}))  # ou recipe.pk # noqa:E501

        self.assertEqual(response.status_code, 404)
