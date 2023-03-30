from django.test import TestCase

from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    # Esse teste sempre é executado antes de cada teste
    def setUp(self) -> None:

        return super().setUp()

    def make_category(self, name='Category'):  # Cria a categoria com o nome Category # noqa:E501
        return Category.objects.create(name=name)

    def make_author(self,  # Cria um author # noqa:E501
                    first_name='user',
                    last_name='name',
                    username='username',
                    password='123456',
                    email='username@email.com'
                    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(self,  # Cria a recipe(receita)_ # noqa:E501
                    category_data=None,
                    # authos criado acima
                    author_data=None,
                    title='Recipe Title',
                    description='Recipe Description',
                    slug='recipe-slug',
                    preparation_time=10,
                    preparation_time_unit='Minutos',
                    servings=3,
                    servings_unit='Perções',
                    preparation_step='Recipe Preparation Steps',
                    preparation_step_is_html=False,
                    is_published=True,
                    ):
        if category_data is None:
            category_data = {}
        if author_data is None:
            author_data = {}
        return Recipe.objects.create(  # noqa: F841
            category=self.make_category(**category_data),  # **category_data transforma todas as chaves de um dicionario ou ele ficara vazio# noqa:E501
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_step=preparation_step,
            preparation_step_is_html=preparation_step_is_html,
            is_published=is_published,
        )
