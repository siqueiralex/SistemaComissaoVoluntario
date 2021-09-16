from django.forms import ModelForm
from django import forms
from projetos.models import Cronograma
from django.utils.timezone import now

class HomologacaoForm(forms.Form):
    file = forms.FileField()
    dia = forms.DateTimeField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date"})) 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dia'].widget.attrs['class']="form-control"
        

class AtestoImpedimentoForm(forms.Form):
    file = forms.FileField()
    inicio = forms.DateTimeField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date"}))
    fim = forms.DateTimeField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date"}))
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['inicio'].widget.attrs['class']="form-control"
        self.fields['fim'].widget.attrs['class']="form-control"

class DistribuicaoForm(forms.Form):
    file = forms.FileField()
    dia = forms.DateTimeField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date"}))
    linha_header = forms.IntegerField()
    nome_aba = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nome_aba'].widget.attrs['value'] = "Classificação"
        self.fields['linha_header'].widget.attrs['value'] = 1
        for field in self.fields.keys():
            self.fields[field].widget.attrs['required']="True"

        self.fields['nome_aba'].widget.attrs['class'] = "form-control"
        self.fields['linha_header'].widget.attrs['class'] = "form-control"
        self.fields['dia'].widget.attrs['class'] = "form-control"
        
    