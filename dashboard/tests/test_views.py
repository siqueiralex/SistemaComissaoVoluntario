from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

class TestViews(TestCase):
    
    def setUp(self):
        self.group = Group(name="Comissao")
        self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        

    def test_cronogramas_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:cronogramas'))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_criar_cronograma_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:criar_cronograma'))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_cronograma_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))

    def test_editar_cronograma_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:editar_cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_apagar_cronograma_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:apagar_cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_exportar_projetos_excel_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:exportar_projetos_excel', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_exportar_vagas_excel_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:exportar_vagas_excel', args=[1,'dia']))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))

    def test_atividades_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:atividades', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_criar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:criar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))

    def test_editar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:editar_atividade', args=[1,1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_apagar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('dashboard:apagar_atividade', args=[1,1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
        
    def test_cronogramas_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:cronogramas'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_criar_cronograma_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:criar_cronograma'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_cronograma_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_editar_cronograma_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:editar_cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_apagar_cronograma_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:apagar_cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_atividades_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:atividades', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_criar_atividade_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:criar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_editar_atividade_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:editar_atividade', args=[1,1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_apagar_atividade_not_comissao_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('dashboard:apagar_atividade', args=[1,1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))





    
    
    
