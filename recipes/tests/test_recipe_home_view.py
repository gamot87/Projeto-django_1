from unittest import skip  # noqa: F401

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


# @skip('Pular testes abaixo')
# Importamos as views
# Create your tests here.
# RecipeViewsTest está herdando de RecipeTestBase(do arquivo test_recipe_base) os metodos(e todos os metodos de TestCase) e ainda sim é um objeto TestCase # noqa:E501
class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_functions_is_correct(self):
        view = resolve(reverse('recipes:home'))
        # estamos perguntando de view.func é = views.home
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_code_200_OK(self):
        # client serve para simular um usuario que irá fazer um request na url especificada # noqa:E501
        response = self.client.get(reverse('recipes:home'))
        # status_code é uma informação que temos na variavel response, ela pode ser verificada fazendo o debug com break point # noqa:E501
        # na linha abaixo e verificar em depurar (3 icone de cima para baixo, apos a lupa) quais propiedades a variavel tem # noqa:E501
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view__loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    # @skip('pula somente o primeiro teste')
    def test_recipe_home_shows_no_recipes_found_if_no_recipes(self):
        # para todos os testes existe uma receita que foi gerada no setUp que é executado antes de todos os testes # noqa:E501
        # entao temos que teletar ela para esse teste
        # Recipe.objects.get(pk=1).delete()
        # Testar se na view home nao houver receitas ele exibirá a mensagem 'No recipes found' # noqa:E501
        # vamos no concole de depuração e executamos o comando response.content.decode('utf-8') # noqa:E501
        # para ver o conteudo da variavel em forma de string
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )

        # Podemos usar o self.fail para nos lembrar de terminar de digitar um codigo # noqa:E501
        # self.fail('Para que eu termine de digitá-lo')

    def test_recipe_home_template_loads_recipes(self):
        # Testa se existe uma receita
        # Vamos chamar o metodo herdado de test_rtecipe_base que cria uma receita: # noqa:E501
        self.make_recipe(author_data={
            'first_name': 'Gabriel'
        })  # aqui usamos um dicionario para dar valores em author_data e category_data do metodo no arquivo test_recipe_base # noqa:E501
        # *no debug console podemos acessar os items criados (context)
        # response.context[‘recipes’].first().nomevariavel
        response = self.client.get(reverse('recipes:home'))
        response_recipes = response.context['recipes']
        # Verifica se o numero de recipe criado foi 1 ou seja, confirma que a recipe foi criada # noqa:E501
        # self.assertEqual(len(response.context['recipes']), 1)
        # Veritica se o tittle da receita é 'Recipe Title'
        # self.assertAlmostEqual(
        # response_recipes.first().title, 'Recipe Title')
        content = response.content.decode('utf-8')
        # Checar se algum conteudo especifico (title = 'Recipe Title' que foi criado junto com a receita) # noqa:E501
        # está em content, que foi transformado em string acima # noqa:E501
        self.assertIn('Gabriel',
                      content)
        self.assertIn('Recipe Title',
                      content)
        self.assertIn('10 Minutos',
                      content)
        # Testando se temos somente uma receita , para ter certeza que ela foi criada e exibida # noqa:E501
        self.assertEqual(len(response_recipes), 1)

    def test_recipe_home_template_dont_load_recipes_not_published(self):
        # test if recipe is_published = False dont show
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))

        self.assertIn(
            '<h1>No recipes found here</h1>',
            response.content.decode('utf-8')
        )
