# Sistema de Apoio à Comissão de Serviço Voluntário

Para máquinas Linux, é necessário que tenha instalado Python 3.8 e as libs: 'libpq-dev' e 'python-dev'

Para demais situações, pesquisar libs necessárias para que o PostgreSQL funcione bem com Python3.8

## Instruções de Deploy

1 - Clone o projeto

2 - Se for utilizar um banco de dados PostgreSQL, adicione as variaveis de ambiente: DB_NAME, DB_USER, DB_PASSWORD e DB_HOST

3 - Se NÃO for utilizar PostgreSQL, remova do arquivo requirements.txt a linha com o psycopg2

4 - Instale as bibliotecas contidas no arquivo requirements.txt (recomendo utilizar um virtualenv)

5 - Caso queira utilizar banco SQLite3, edite o arquivo voluntario/settings/production.py comentando a parte de postgresql e descomentando a parte de SQLite (o passo 3 será desnecessário nesse caso)

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

8 - Gere os arquivos estaticos com o comando:

```
python manage.py collectstatic
```


8 - Para rodar e testar o sistema localmente o comando é o seguinte:
```
python manage.py runserver --insecure
```

Você poderá acessar o sistema localmente na porta 8000 do localhost!

