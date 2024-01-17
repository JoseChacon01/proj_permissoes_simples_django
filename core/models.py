from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    cpf = models.CharField('cpf', max_length=11, unique=True)
    nome = models.CharField('nome', max_length=100)
    idade = models.IntegerField('idade')

    USERNAME_FIELD = 'cpf'

    class Meta:
        permissions = [
            ('professor', 'Permissão de Usuários Professores'),
            ('aluno', 'Permissão de Usuários Alunos')
        ]