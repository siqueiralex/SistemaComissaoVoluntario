# Sistema de Apoio à Comissão de Serviço Voluntário
## Instruções de Deploy
### Para rodar localmente:

1 - Clone o projeto

2 - Crie um virtualenv de Python3.8 e instale os requirements do arquivo requirements.txt

3 - Criar dentro da pasta voluntario/settings/ o arquivo development.py a partir do exemplo contido na pasta

4 - Co recém-criado development.py, troque os dados de banco de dados para um banco postgresql local vazio (para outro tipo de banco altere a ENGINE


5 - Exporte a variável de ambiente conforme exemplo abaixo OU insira em todos os comandos seguintes a diretiva  '--settings voluntario.settings.development'

```
export DJANGO_SETTINGS_MODULE="voluntario.settings.development"
```


6 - Faça o setup do banco de dados com os comandos:
```
python manage.py makemigrations
python manage.py migrate
```

7 - Os dados iniciais do banco serão adicionados pelos comandos:
```
python manage.py loaddata fixtures/1-usuarios.json
python manage.py loaddata fixtures/2-projetos.json
```

8 - Para rodar o sistema localmente o comando é o seguinte:
```
python manage.py runserver
```

Pronto! Você poderá acessar o sistema localmente na porta 8000 do localhost!


### Para fazer deploy com ASGI ou WSGI:

1 - Clone o projeto

2 - Crie um virtualenv de Python3.8 e instale os requirements do arquivo requirements.txt

3 - Exporte a variável de ambiente DJANGO_SETTINGS_MODULE com o valor 'voluntario.settings.production'
export DJANGO_SETTINGS_MODULE="voluntario.settings.production"

4 - Exporte as variáveis DB_NAME, DB_USER, DB_PASSWORD DB_HOST com os valores referentes a um DB postgresql vazio
export DB_NAME_ALEX="db_voluntario_alex"
export DB_USER_ALEX="voluntario_alex"
export DB_PASSWORD_ALEX="v0luntar10@lex"
export DB_HOST_ALEX="10.233.161.9"

Obs: caso queira alterar a forma de injetar as credenciais ou o tipo de DB, altere diretamente os dados no arquivo voluntario/settings/production.py

6 - Faça o setup do banco de dados com os comandos:
```
python manage.py makemigrations
python manage.py migrate
```

7 - Os dados iniciais do banco serão adicionados pelos comandos:
```
python manage.py loaddata fixtures/1-usuarios.json
python manage.py loaddata fixtures/2-projetos.json
```
