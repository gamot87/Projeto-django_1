# sabendo que a fila de numeros de paginas começa a mudar a partir da página 3 usarmos uma condição if # noqa:E501


# minha solução:
import math

'''def make_pagination_range(
        page_range,
        qty_pages,
        current_page):

    if current_page > 2 and current_page < max(page_range) - 1:
        return [current_page - 1, current_page, current_page + 1, current_page+2]  # noqa:E501
    elif current_page == max(page_range) - 1:
        return [current_page - 2, current_page - 1, current_page, current_page + 1]  # noqa:E501
    elif current_page >= max(page_range):
        return [max(page_range)-3, max(page_range)-2, max(page_range)-1, max(page_range)]  # noqa:E501
    else:
        return [1, 2, 3, 4]'''

# INCLUINDO PAGINATION E OS VALORES DAS VARIAVEIS DA FUNÇÂO:


'''def make_pagination_range(
        page_range,
        qty_pages,
        current_page):
    total_pages = max(page_range)
    pagination = []
    if current_page > 2 and current_page < max(page_range) - 1:
        pagination = [current_page - 1, current_page, current_page + 1, current_page+2]  # noqa:E501

    elif current_page == max(page_range) - 1:
        pagination = [current_page - 2, current_page - 1, current_page, current_page + 1]  # noqa:E501

    elif current_page >= max(page_range):
        pagination = [max(page_range)-3, max(page_range)-2, max(page_range)-1, max(page_range)]  # noqa:E501

    else:
        pagination = [1, 2, 3, 4]

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'total_pages': total_pages,
        'start_range': pagination[0],
        'stop_range': pagination[3],
        'first_page_out_of_range': current_page > 2,
        'last_page_out_of_range': current_page < max(page_range) -2
    }'''


# Solução do professor
def make_pagination_range(
        page_range,
        qty_pages,
        current_page):

    middle_range = math.ceil(qty_pages/2)  # math.ceil arredonda para cima
    start_range = current_page - middle_range
    stop_range = current_page + middle_range
    total_pages = len(page_range)  # ou max(page_range)
    # numero absoluto(positivo) de start range se start range for negativo caso contrario ele assume o valor de 0 # noqa:E501
    start_range_offset = abs(start_range) if start_range < 0 else 0

    if start_range < 0:
        start_range = 0
        stop_range += start_range_offset
    if stop_range >= total_pages:
        start_range = start_range - abs(total_pages - stop_range)

    pagination = page_range[start_range:stop_range]
    # fazemos um fatiamento para que seja exibido somente 4 elementos dependendo do intervalo que desejamos # noqa:E501
    # È IMPORTANTE MENCIONAR QUE SE VALOR DE stop_range FOR MAIOR QUE O RANGE DA LISTA ELA SOMENTE EXIBIRÁ ATÉ # noqa:E501
    # 0 VALOR MAXIMO DELA max(page_range) QUE É 20 MESMO QUE stop_range TENHA VALOR DE 30 POR EXEMPLO # noqa:E501
    # return page_range[start_range:stop_range] ou pagination = page_range[start_range:stop_range] # noqa:E501

    return {
        'pagination': pagination,
        'page_range': page_range,
        'qty_pages': qty_pages,
        'total_pages': total_pages,
        'start_range': start_range,
        'stop_range': stop_range,
        'first_page_out_of_range': current_page > middle_range,
        'last_page_out_of_range': stop_range < total_pages,
    }
