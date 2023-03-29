from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=65)
    # a função abaixo permite que na area administrativa apareça o nome da
    # categoria e nao o seu id

    def __str__(self):
        return self.name


class Recipe(models.Model):
    # Cada atributo abaixo tem o valor de uma coluna e suas caracteristicas.
    # Charfield = campo de caracteres , com no maximo 65 caracteres
    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    # slug é uma variável especial , ela tem como caracteristica ser indexada
    # ou seja , podemos identificar registros por ela
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(max_length=15)
    servings = models.IntegerField()
    servings_unit = models.CharField(max_length=15)
    # TextField significa Campo para texto com caracteres ilimitados
    preparation_step = models.TextField()
    preparation_step_is_html = models.BooleanField(default=False)
    # o codigo abaixo faz com que somente
    # no momento da criação a data seja salva
    created_at = models.DateTimeField(auto_now_add=True)
    # o codigo abaixo faz com que as datas dos updates sejam salvas
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    # o codigo abaixo salva as imagens na pasta com a data do dia, por
    # isso temos %Y/%m/%d para que ele procure a pasta com o nome igual
    # a data do dia
    # blank=True,default='' tira aobrigatoriedade de foto e coloca uma
    # string vazia no lugar
    cover = models.ImageField(
        upload_to='recipes/covers/%Y/%m/%d', blank=True, default='')
    # abaixo temos uma coluna com valor de chave estrangeira ou seja temos
    # um relacionamento com outra tabela, no caso a tabela Category .
    # on_delete=models.SET_NULL significa que se a tabela Category for apagado
    # o campo será preenchido com valores nulos.
    # null=True significa que pode receber valores nulos.
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        null=True,
        blank=True,
        default=None,
    )
    # Abaixo a coluna author recebe o nome de usuario automaticamente
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True
    )

    def __str__(self):
        return self.title
