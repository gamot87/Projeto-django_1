from django.core.exceptions import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        # vamos mudar o title da receita para ultrapassar os 65 characteres # noqa:E501
        self.recipe.title = "A" * 70  # * multiplica a string ou seja teremos A multiplicado # noqa:E501

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()  # a verificação do tamanho do tittle será feita nessa linha de codigo .fullclean() # noqa : E501
        # o codig abaixo é importante para que seja salvo esse novo titulo
        # self.recipe.save()
        # o codigo abaixo cria uma falha para que possamos verificar se o titulo foi alterado na linha com o erro assertionError # noqa:E501
        # self.fail(self.recipe.title)

    # Abaixo usamos a ferramenta @parameterized para criar um teste para cada valor de tupla # noqa:E501

    def make_recipe_no_defaults(self):
        recipe = Recipe(  # noqa:F841
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(
                    username='newusername',  # alteramos somente o username pq ja estamos criando um usuario para todos os testes com a funão setUp # noqa:E501
                    ),
            title='Recipe Title',
            description='Recipe Description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=3,
            servings_unit='Perções',
            preparation_step='Recipe Preparation Steps',
            )
        recipe.full_clean()  # ocorre as validações
        recipe.save()
        return recipe

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 15),
        ('servings_unit', 15),
    ])
    def test_recipe_fields_max_lenght(self, field, max_lenght):  # (field, max_lenght sao respectivamente o primeiro e o segundo valor de cada tupla acima # noqa:E501
        setattr(self.recipe, field, 'A' * (max_lenght + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.preparation_step_is_html,
            msg='Recipe preparation_step_is_html is not False'
            )  # agora sim vamos testar se o campo preparation_step_is_html é falso # noqa:E501

    def test_recipe_is_published_is_false_by_default(self):
        recipe = self.make_recipe_no_defaults()
        self.assertFalse(
            recipe.is_published,
            msg='Recipe is_published is not False'
        )
