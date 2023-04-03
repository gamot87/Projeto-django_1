from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category Testing'
        )
        return super().setUp()

    def test_recipe_category_string_represetation_is_name_field(self):
        # testando se o nome da categoria quando criada é realmente o nome que colocamos no name ao criar # noqa : E501
        self.assertEqual(
            str(self.category),
            self.category.name,  # substituimos essa linha por (self.category.name + ' ') de forma a acrescentar um espaço e entao ficarem diferentes # noqa : E501
        )

    def test_recipe_category_model_name_max_lenght_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
