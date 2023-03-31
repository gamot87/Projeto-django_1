from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


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
