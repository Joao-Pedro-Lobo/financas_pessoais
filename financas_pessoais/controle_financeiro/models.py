from django.db import models
from django.utils import timezone

class ControleModel(models.Model):
    Nome = models.CharField(max_length=100)
    Descrição = models.TextField(null=True, blank=True,max_length=1200 )
    CATEGORIA_CHOICES = (
        ('1', 'Educação'),
        ('2', 'Água'),
        ('3', 'Luz'),
        ('4', 'Aluguel'),
        ('5', 'Comida'),
        ('6', 'Lazer'),
        ('7', 'Internet'),
        ('8', 'Outros'),
    )
    Categoria = models.CharField(max_length=1, choices=CATEGORIA_CHOICES)
    Preço = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    Data = models.DateField(default=timezone.now)

    def __str__(self):
        return self.Nome