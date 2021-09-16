from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('distribuicao/', views.distribuicao, name="distribuicao"),
    path('atesto-impedimentos/', views.atesto_impedimentos, name="atesto_impedimentos"),
    path('homologacoes/', views.homologacoes, name="homologacoes"),

]


