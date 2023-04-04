from unittest import skip  # noqa: F401

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# @skip('Pular testes abaixo')
# Importamos as views
# Create your tests here.
# RecipeViewsTest está herdando de RecipeTestBase(do arquivo test_recipe_base) os metodos(e todos os metodos de TestCase) e ainda sim é um objeto TestCase # noqa:E501
class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_functions_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 10000}))
        # estamos perguntando de view.func é = views.home
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_returns_404_if_no_recipes_found(self):  # noqa:E501
        # client serve para simular um usuario que irá fazer um request na url especificada # noqa:E501
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100000}))
        # status_code é uma informação que temos na variavel response, ela pode ser verificada fazendo o debug com break point # noqa:E501
        # na linha abaixo e verificar em depurar (3 icone de cima para baixo, apos a lupa) quais propiedades a variavel tem # noqa:E501
        self.assertEqual(response.status_code, 404)

    def teste_recipe_Category_template_loads_recipes(self):
        # Testa se existe uma category
        needed_title = 'this is a category test'
        self.make_recipe(title=needed_title)  # mudamos o title para testar se ele gera um igual # noqa:E501
        response = self.client.get(reverse('recipes:category', kwargs={
            'category_id': 1
        }
        ))
        content = response.content.decode('utf-8')
        self.assertIn(needed_title,
                      content)

    def test_recipe_category_template_dont_load_recipes_not_published(self):
        # test if recipe is_published = False dont show
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': recipe.category.id}))

        self.assertEqual(response.status_code, 404)
