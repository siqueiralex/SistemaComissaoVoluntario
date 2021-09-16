# Sistema de Apoio à Comissão de Serviço Voluntário

## Instruções de Deploy

1 - Clone o projeto

2 - Crie um virtualenv de Python3.8 e instale as bibliotecas contidas no arquivo requirements.txt

3 - Se for utilizar um banco de dados Postgresql, adicione as variaveis de ambiente: DB_NAME, DB_USER, DB_PASSWORD e DB_HOST.

4 - Caso queira utilizar banco SQLite3, edite o arquivo voluntario/settings/production.py comentando a parte de postgresql, e descomentando a parte de SQLite

6 - Faça o primeiro setup do banco de dados com os comandos:
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

Você poderá acessar o sistema localmente na porta 8000 do localhost!

