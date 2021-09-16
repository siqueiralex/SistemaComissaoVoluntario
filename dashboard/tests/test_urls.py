from django.test import SimpleTestCase
from django.urls import reverse, resolve
from dashboard.views import *
from dashboard.reports.views import *

class TestUrls(SimpleTestCase): 

    
    def test_cronogramas_resolves(self):
        url = reverse('dashboard:cronogramas')
        self.assertEquals(resolve(url).func, cronogramas)
    
    def test_criar_cronograma_resolves(self):
        url = reverse('dashboard:criar_cronograma')
        self.assertEquals(resolve(url).func, criarCronograma)
    
    def test_cronograma_resolves(self):
        url = reverse('dashboard:cronograma', args=[1])
        self.assertEquals(resolve(url).func, cronograma)
    
    def test_apagar_cronograma_resolves(self):
        url = reverse('dashboard:apagar_cronograma', args=[1])
        self.assertEquals(resolve(url).func, apagarCronograma)
    
    def test_editar_cronograma_resolves(self):
        url = reverse('dashboard:editar_cronograma', args=[1])
        self.assertEquals(resolve(url).func, editarCronograma)
    
    def test_exportar_vagas_excel_resolves(self):
        url = reverse('dashboard:exportar_vagas_excel', args=[1,'dia'])
        self.assertEquals(resolve(url).func, exportarVagasExcel)

    def test_exportar_projetos_excel_resolves(self):
        url = reverse('dashboard:exportar_projetos_excel', args=[1])
        self.assertEquals(resolve(url).func, exportarProjetosExcel)


    def test_atividades_resolves(self):
        url = reverse('dashboard:atividades', args=[1,1])
        self.assertEquals(resolve(url).func, atividades)
   
    def test_criar_atividade_resolves(self):
        url = reverse('dashboard:criar_atividade', args=[1,1])
        self.assertEquals(resolve(url).func, criarAtividade)
    
    def test_editar_atividade_resolves(self):
        url = reverse('dashboard:editar_atividade', args=[1,1,1])
        self.assertEquals(resolve(url).func, editarAtividade)
    
    def test_apagar_atividade_resolves(self):
        url = reverse('dashboard:apagar_atividade', args=[1,1,1])
        self.assertEquals(resolve(url).func, apagarAtividade)