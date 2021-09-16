from django.contrib.auth import views as auth_views
from django.urls import path, include
from . import views
from . import reports

urlpatterns = [

    path('alterar-senha/', views.alterar_senha.as_view(), name="alterar_senha" ),
    path('login/', views.login, name="login" ),
    path('logout/', views.logout, name="logout"),  
    path('cronograma/', include([

            # CRONOGRAMA
            path('', views.cronogramas, name="cronogramas"),
            path('criar/', views.criarCronograma, name="criar_cronograma"),
            path('<cron_id>/', views.cronograma, name="cronograma"),
            path('<cron_id>/confirma_apagar/', views.confirmaApagarCronograma, name="apagar_cronograma_confirma"),
            path('<cron_id>/apagar/', views.apagarCronograma, name="apagar_cronograma"),
            path('<cron_id>/editar/', views.editarCronograma, name="editar_cronograma"),
            path('<cron_id>/exportar_vagas_excel/<dia>/', reports.exportarVagasExcel, name="exportar_vagas_excel"),
            path('<cron_id>/exportar_projetos/', reports.exportarProjetosExcel, name="exportar_projetos_excel"),    

            # PROJETO DE UNIDADE DEMANDANTE
            path('<cron_id>/unidade/<un_id>/atividade/', include([     
                path('', views.atividades, name="atividades"),
                path('criar/', views.criarAtividade, name="criar_atividade"),
                path('<ativ_id>/editar/', views.editarAtividade, name="editar_atividade"),
                path('<ativ_id>/apagar/', views.apagarAtividade, name="apagar_atividade"),
            ])),


        ])),

]