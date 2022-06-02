from django.db import models

# Create your models here.
class Automato(models.Model):
    Alfabeto = models.CharField(max_length=9999)
    Estados = models.CharField(max_length=9999)
    EstadoInicial = models.CharField(max_length=9999)
    EstadosDeAceitacao = models.CharField(max_length=9999)
    DicionarioTransicao = models.CharField(max_length=9999)
    Descricao = models.CharField(max_length=9999)

    def __str__(self):
        return self.Descricao[:30]

class MaquinaTuring(models.Model):
    Alfabeto = models.CharField(max_length=9999)
    Estados = models.CharField(max_length=9999)
    EstadoInicial = models.CharField(max_length=9999)
    EstadosDeAceitacao = models.CharField(max_length=9999)
    DicionarioTransicao = models.CharField(max_length=9999)
    Descricao = models.CharField(max_length=9999)

    def __str__(self):
        return self.Descricao[:30]