from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import views as auth_views
from django.contrib.auth import authenticate, login as login_user, logout as logout_user
from .forms import *
from .models import *
from .decorators import *
from django.db.models import Count
from itertools import chain

@unauthenticated_user
def login(request):
    context={}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login_user(request, user)
            return redirect('cronogramas')
        else:
            context['login_error'] = "usuário/senha inválidos"
            
    return render(request, "auth/login.html", context)

@login_required(login_url='login')
def logout(request):
    logout_user(request)
    return redirect('login')


class alterar_senha(auth_views.PasswordChangeView):
    template_name = "auth/alterar_senha.html"
    success_url = '/'


@login_required(login_url='login')
def cronogramas(request):
    context = {}
    cronogramas = Cronograma.objects.all()
    if cronogramas:
        context['ultimo_cadastrado'] = cronogramas[:1][0]
        context['cronogramas'] = cronogramas[1:]
    
 
    return render(request, 'projetos/cronogramas.html', context)

@login_required(login_url='login')
def cronograma(request, cron_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    context = {}

    unidades = list(Unidade.objects.values())
    atividades = cronograma.atividade_set.all()

    for unidade in unidades:
        unidade['qtde_atividades'] = atividades.filter(unidade_id=unidade['id']).count()

    print(unidades)
    

    
    context['unidades'] = unidades
    context['cronograma'] = cronograma
    return render(request, 'projetos/cronograma.html', context)

@login_required(login_url='login')
def criarCronograma(request):
    form = CronogramaForm()

    if request.method == "POST":
        form = CronogramaForm(request.POST)
        if form.is_valid():
            form.save()    
            return redirect('cronogramas')

    context = {'form':form }
    return render(request, 'projetos/cronograma_form.html', context)

@login_required(login_url='login')
def editarCronograma(request, cron_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    
    form = CronogramaForm(instance=cronograma)
    if request.method == "POST":

        form = CronogramaForm(request.POST, instance=cronograma)
        
        if form.is_valid():
            cronograma = Cronograma.objects.get(id=form.instance.id)
            if form.cleaned_data['inicio_servicos'] != cronograma.inicio_servicos or form.cleaned_data['fim_servicos'] != cronograma.fim_servicos:
                if cronograma.atividade_set.exists():
                    messages.warning(request, "Você não pode alterar um período que já tem atividades enviadas. Apague as atividades manualmente antes de fazê-lo.")
                    return render(request, 'projetos/cronograma_form.html', {'form':form})
                
            form.save()    
            return redirect('cronogramas')

    context = {'form':form }
    return render(request, 'projetos/cronograma_form.html', context)


@login_required(login_url='login')
def confirmaApagarCronograma(request, cron_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    context = {'cronograma':cronograma}
    
    return render(request, 'projetos/cronograma_apagar_confirmacao.html', context)


@login_required(login_url='login')
def apagarCronograma(request, cron_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    
    
    if cronograma.atividade_set.exists():
        messages.warning(request, "Este periodo tem atividades enviadas e não pode ser apagado. Apague as atividades manualmente antes de fazê-lo.")
        return redirect('cronogramas')

    cronograma.delete()
    messages.warning(request, f"Período '{cronograma}'' apagado!")
    return redirect('cronogramas')


@login_required(login_url='login')
def atividades(request, cron_id, un_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    unidade = Unidade.objects.get(id=un_id)
    atividades = Atividade.objects.filter(unidade = unidade, cronograma=cronograma)
    
    
    context = { 'cronograma':cronograma, 'unidade':unidade, 'atividades':atividades}
    return render(request, 'projetos/atividades.html', context)


@login_required(login_url='login')
def criarAtividade(request, cron_id, un_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    unidade = Unidade.objects.get(id=un_id)

    dias = cronograma.quantidade_de_dias
    form = AtividadeForm()
    
    EfetivoDiarioFormSet = inlineformset_factory(Atividade, EfetivoDiario, form=EfetivoDiarioForm, fields=('dia', 'efetivo'), can_delete=False, extra=dias) #extra=quantidadededias
    formset = EfetivoDiarioFormSet() 
    

    datas = cronograma.lista_de_datas
    for i in range(0,dias):
        formset.forms[i].fields['dia'].initial = datas[i]
        
    if request.method == "POST":
        form = AtividadeForm(request.POST)
        if form.is_valid():
            atividade = form.save(commit=False)
            atividade.unidade = unidade
            atividade.cronograma = cronograma
            
            formset = EfetivoDiarioFormSet(request.POST, instance=atividade)
            if formset.is_valid():
                atividade.save()    
                formset.save()

                messages.success(request, f"Atividade {atividade.nome} foi criada!")

                return redirect('atividades', cron_id=cron_id, un_id=un_id)


    context = {
        'cronograma':cronograma,
        'unidade':unidade,
        'form':form,
        'formset':formset
        }
    return render(request, 'projetos/atividade_form.html', context)

@login_required(login_url='login')
def editarAtividade(request, cron_id, un_id, ativ_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    unidade = Unidade.objects.get(id=un_id)
    atividade = Atividade.objects.get(id=ativ_id)


    # alterar ids na URL = curto-circuito
    if atividade.cronograma.id != int(cron_id):
        return redirect('atividades', cron_id=cron_id, un_id=un_id)

    # alterar ids na URL = curto-circuito
    if atividade.unidade.id != int(un_id):
        return redirect('atividades', cron_id=cron_id, un_id=un_id)

    form = AtividadeForm(instance=atividade)    
    EfetivoDiarioFormSet = inlineformset_factory(Atividade, EfetivoDiario,form=EfetivoDiarioForm, fields=('dia', 'efetivo'), can_delete=False, extra=0)
    formset = EfetivoDiarioFormSet(instance=atividade) 


    if request.method == "POST":
        form = AtividadeForm(request.POST, instance=atividade)
        if form.is_valid():
            formset = EfetivoDiarioFormSet(request.POST, instance=atividade)
            
            
            if formset.is_valid():    
                form.save()
                formset.save()
                return redirect('atividades',cron_id=cron_id, un_id=un_id )

    context = {
        'cronograma':cronograma,
        'unidade':unidade,
        'form':form,
        'formset':formset
        }

    return render(request, 'projetos/atividade_form.html', context)


@login_required(login_url='login')
def apagarAtividade(request, cron_id, un_id, ativ_id):
    cronograma = Cronograma.objects.get(id=cron_id)
    unidade = Unidade.objects.get(id=un_id)
    atividade = Atividade.objects.get(id=ativ_id)

   # alterar ids na URL = curto-circuito
    if atividade.cronograma.id != int(cron_id):
        return redirect('atividades', cron_id=cron_id, un_id=un_id)

    # alterar ids na URL = curto-circuito
    if atividade.unidade.id != int(un_id):
        return redirect('atividades', cron_id=cron_id, un_id=un_id)

    messages.warning(request, f"Atividade {atividade.nome} foi apagada!")

    atividade.delete()
    return redirect('atividades', cron_id=cron_id, un_id=un_id)