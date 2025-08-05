from django import forms
from .models import ControleModel

class ControleForm(forms.ModelForm):
    class Meta:
        model = ControleModel
        fields = ['Nome', 'Descrição', 'Categoria', 'Preço', 'Data'] 