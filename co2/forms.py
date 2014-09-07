from django import forms
from django.forms.models import inlineformset_factory
from .models import *

class EntidadForm(forms.ModelForm):
    class Meta:
        model = Entidad

class ConsumoForm(forms.ModelForm):
    class Meta:
        model = Consumo

ConsumosFormSet = inlineformset_factory(Entidad, Consumo)