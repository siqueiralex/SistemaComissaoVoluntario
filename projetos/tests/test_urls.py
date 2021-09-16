from django.test import SimpleTestCase
from django.urls import reverse, resolve
from projetos.views import *

class TestUrls(SimpleTestCase):

    def test_index_resolves(self):
        url = reverse('index')
        self.assertEquals(resolve(url).func, index) 
    
    def test_login_resolves(self):
        url = reverse('login')
        self.assertEquals(resolve(url).func, login ) 
    
    def test_logout_resolves(self):
        url = reverse('logout')
        self.assertEquals(resolve(url).func, logout)
    
    def test_alterar_senha_resolves(self):
        url = reverse('alterar_senha')
        self.assertEquals(resolve(url).func.view_class, alterar_senha)
    
    def test_cronogramas_resolves(self):
        url = reverse('cronogramas')
        self.assertEquals(resolve(url).func, cronogramas)
    
    def test_cronograma_resolves(self):
        url = reverse('cronograma', args=[1])
        self.assertEquals(resolve(url).func, cronograma)
    
    def test_atividades_resolves(self):
        url = reverse('atividades', args=[1])
        self.assertEquals(resolve(url).func, atividades)
   
    def test_criar_atividade_resolves(self):
        url = reverse('criar_atividade', args=[1])
        self.assertEquals(resolve(url).func, criarAtividade)
    
    def test_editar_atividade_resolves(self):
        url = reverse('editar_atividade', args=[1,1])
        self.assertEquals(resolve(url).func, editarAtividade)
    
    def test_apagar_atividade_resolves(self):
        url = reverse('apagar_atividade', args=[1,1])
        self.assertEquals(resolve(url).func, apagarAtividade)