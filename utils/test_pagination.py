# Apesar de ter o mesmo nome da classe que importamos do django.test
# essa classe importada do unittes éum pouco mais simples nos asserts
from unittest import TestCase

from utils.pagination import make_pagination_range


# queremos que os numeros das paginas fiquem como no google, exemplo: 1 2 3 4 e a pagina que estamos em azul, e que ela avance para 5  # noqa:E501
# quando a pagina atual for 3 e assim m por diante até a pagina 20 , onde na pagina 19 e 20 deve-se obter 17,18,19,20 pois nosso range é de 20  # noqa:E501
# paginas entao nao é possivel avançar, enfim, vamos testar essa logica  # noqa:E501
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
