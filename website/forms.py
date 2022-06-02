from django.forms import ModelForm

from .models import Automato, MaquinaTuring
from django import forms


class AutomatoForm(ModelForm):
    class Meta:
        model = Automato
        fields = '__all__'

class MaquinaTuringForm(ModelForm):
    class Meta:
        model = MaquinaTuring
        fields = '__all__'

class ObterSequenciaForm(forms.Form):
    Sequencia = forms.CharField(label='Obter sequencia', max_length=999)