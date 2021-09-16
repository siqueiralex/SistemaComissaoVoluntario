from django.contrib.auth.models import User, Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import *
from .decorators import *

@receiver(post_save, sender=EfetivoDiario)
@disable_for_loaddata
def efetivo_saved(sender, instance, created, **kwargs):
    args = {}
    
    if created:
        for i in range(instance.efetivo):
            Vaga.objects.create(generator = instance, 
            unidade= instance.atividade.unidade, 
            dia = instance.dia,
            atividade = instance.atividade.nome,
            tipo_atividade = instance.atividade.tipo_atividade,
            responsavel = instance.atividade.responsavel,
            carga_horaria = instance.atividade.carga_horaria,
            horario = instance.atividade.horario 
            )
    else:

        antigas = Vaga.objects.filter(generator = instance)
        antigas.update(
                unidade= instance.atividade.unidade, 
                dia = instance.dia,
                atividade = instance.atividade.nome,
                tipo_atividade = instance.atividade.tipo_atividade,
                responsavel = instance.atividade.responsavel,
                carga_horaria = instance.atividade.carga_horaria,
                horario = instance.atividade.horario)

        qtde_atual = antigas.count()
        if instance.efetivo > qtde_atual:
            delta = instance.efetivo - qtde_atual
            for i in range(delta):
                Vaga.objects.create(generator = instance, 
                unidade= instance.atividade.unidade, 
                dia = instance.dia,
                atividade = instance.atividade.nome,
                tipo_atividade = instance.atividade.tipo_atividade,
                responsavel = instance.atividade.responsavel,
                carga_horaria = instance.atividade.carga_horaria,
                horario = instance.atividade.horario 
                )

        else:
            delta = qtde_atual - instance.efetivo
            excedente = antigas[:delta]
            for e in excedente:
                e.delete()

        

@receiver(post_save, sender=Atividade)
@disable_for_loaddata
def atividade_saved(sender, instance, created, **kwargs):
    if not created:
        for e in instance.efetivodiario_set.all():
            e.save()


# # SUPER USER SEMPRE INTEGRA GRUPO COMISSAO
# @receiver(post_save, sender=User)
# @disable_for_loaddata
# def superuser_created(sender, instance, created, **kwargs):
#     if created:
#         user = instance
#         if user.is_superuser:
#             group = Group.objects.filter(name='Comissao')
#             if group.exists():
#                 user.groups.add(group.first())
        

#Unidade gera um User automaticamente
# @receiver(post_save, sender=Unidade)
# @disable_for_loaddata
# def unidade_created(sender, instance, created, **kwargs):
#     if created:
#         args = {}
#         unidade = instance

#         args['username'] = unidade.sigla.lower()
#         args['password'] = hashlib.sha1(unidade.sigla.encode("ascii")).hexdigest()[:8]

#         user = User.objects.create(**args)
#         group = Group.objects.get(name='Demandante')
#         user.groups.add(group)
#         Unidade.objects.filter(id=instance.id).update(user=user)
