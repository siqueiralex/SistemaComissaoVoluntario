from django.forms import ModelForm
from .models import *
from django import forms
import datetime
from django.utils.timezone import now



class AtividadeForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    

        for field in self.fields.keys():
            self.fields[field].widget.attrs['class'] = "form-control"

        self.fields['horario_inicio'].widget.input_type="time"
        self.fields['horario_fim'].widget.input_type="time"
        self.fields['nome'].widget.attrs['size']="40"
        self.fields['responsavel'].widget.attrs['placeholder']="Responsável pela atividade (curto)"
        self.fields['carga_horaria'].widget.attrs['style']=" text-align:center; "
        # self.fields['carga_horaria'].widget.attrs['min']="0"
        # self.fields['carga_horaria'].widget.attrs['max']="12"
        # self.fields['carga_horaria'].widget.attrs['readonly']="readonly"
        self.fields['horario_inicio'].widget.attrs['style']=" text-align:center; padding-left:10px;"
        self.fields['horario_fim'].widget.attrs['style']="text-align:center; padding-left:10px;"
        self.fields['nome'].widget.attrs['placeholder'] = "Nome da atividade (curto)"



    def clean(self, *args, **kwargs) :
        super(AtividadeForm, self).clean(*args, **kwargs)
        form_data = self.cleaned_data

        inicio = datetime.datetime.combine(datetime.date.today(), form_data['horario_inicio'])
        fim = datetime.datetime.combine(datetime.date.today(), form_data['horario_fim'])
        diff = fim - inicio
        form_data['carga_horaria'] = int(diff.total_seconds()/3600)

        # if int(diff.total_seconds()) != int(form_data['carga_horaria'])*3600:
        #     self._errors["horario_fim"] = ["Horarios inconsistentes com a carga horaria!"]
            
        if int(form_data['carga_horaria']) > 12 or int(form_data['carga_horaria']) < 1 :
            self._errors["horario_fim"] = ["Carga horaria deve ser entre 1 e 12 horas!"]

        return form_data


    class Meta:
        model = Atividade
        fields = '__all__'
        exclude = ['cronograma', 'unidade']
        

class EfetivoDiarioForm(ModelForm):
   
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.keys():
            self.fields[field].widget.attrs['class'] = "form-control"
            self.fields[field].widget.attrs['style'] = "width:100%; font-size: .9em ; text-align:center;border-radius: 0;"

        self.fields['efetivo'].widget.attrs['min'] = "0"
        self.fields['efetivo'].required = True
        self.fields['dia'].widget.attrs['readonly'] = True

    def clean(self, *args, **kwargs) :
        super(EfetivoDiarioForm, self).clean(*args, **kwargs)
        form_data = self.cleaned_data

        if 'efetivo' in form_data:    
            if int(form_data['efetivo']) < 0 :
                self._errors["efetivo"] = ["Efetivo deve ser um número positivo"]

            if int(form_data['efetivo']) > 100:
                self._errors["efetivo"] = ["Número muito grande!"]

        return form_data

        

    class Meta:
        model = EfetivoDiario
        fields = '__all__'
        exclude = ['cronograma', 'unidade']

class CronogramaForm(ModelForm):
    inicio_servicos = forms.DateField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date", "placeholder":"yyyy-mm-dd"}))
    fim_servicos = forms.DateField(input_formats=[f"%Y-%m-%d"], widget=forms.widgets.DateInput(format=f"%Y-%m-%d",attrs={"type":"date", "placeholder":"yyyy-mm-dd"}))        
    
    def clean(self, *args, **kwargs) :
        super(CronogramaForm, self).clean(*args, **kwargs)
        form_data = self.cleaned_data    
        
    
        if form_data['inicio_servicos'] >= form_data['fim_servicos']:
            self._errors["fim_servicos"] = ["Fim deve ser posterior ao inicio"]

        elif form_data['inicio_servicos'].month != form_data['fim_servicos'].month:
            self._errors["fim_servicos"] = ["Período deve estar contidos dentro de um único mês"]
        
        # CHECAR SE O CRONOGRAMA SENDO CRIADO TEM DATAS DENTRO DE DATAS DE OUTRO CRONOGRAMA
        else:
                
            todos_cronogramas = Cronograma.objects.all()
            if self.instance:
                todos_cronogramas = todos_cronogramas.exclude(id=self.instance.id)
            
            for cronograma in todos_cronogramas:
                if (cronograma.inicio_servicos <= form_data['inicio_servicos'] <= cronograma.fim_servicos)\
                    or (cronograma.inicio_servicos <= form_data['fim_servicos'] <= cronograma.fim_servicos):
                    self._errors["fim_servicos"] = ["Novos períodos não podem conter datas de outros períodos."]
            
        
        return form_data
    



    class Meta:
        model = Cronograma
        fields = '__all__'