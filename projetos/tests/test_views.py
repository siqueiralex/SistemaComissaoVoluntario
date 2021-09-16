from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import Group, User

class TestViews(TestCase):
    
    def setUp(self):
        self.group = Group(name="Demandante")
        self.group.save()
        self.c = Client()
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def tearDown(self):
        self.user.delete()
        self.group.delete()
        

    def test_index_unauth_redirect_to_login(self):
        response = self.c.get(reverse('index'))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))

    def test_alterar_senha_unauth_redirect_to_login(self):
        response = self.c.get(reverse('alterar_senha'))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith('/accounts/login/?next=/alterar-senha/')

    def test_cronogramas_unauth_redirect_to_login(self):
        response = self.c.get(reverse('cronogramas'))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_cronograma_unauth_redirect_to_login(self):
        response = self.c.get(reverse('cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_atividades_unauth_redirect_to_login(self):
        response = self.c.get(reverse('atividades', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_criar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('criar_atividade', args=[1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))

    def test_editar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('editar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
    
    def test_apagar_atividade_unauth_redirect_to_login(self):
        response = self.c.get(reverse('apagar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        assert response.url.startswith(reverse('login'))
        

    def test_cronogramas_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('cronogramas'))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_cronograma_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('cronograma', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_atividades_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('atividades', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_criar_atividade_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('criar_atividade', args=[1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))
    
    def test_editar_atividade_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('editar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))

    def test_apagar_atividade_not_demandante_redirect_to_index(self):
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('apagar_atividade', args=[1,1]))
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, reverse('index'))








    def test_cronogramas_demandante_GET(self):
        self.user.groups.add(self.group)
        self.user.save()
        self.c.login(username='test', password='test')
        response = self.c.get(reverse('cronogramas'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'projetos/cronogramas.html')

    
    
    
