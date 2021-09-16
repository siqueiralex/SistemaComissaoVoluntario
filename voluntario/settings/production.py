from voluntario.settings.base import *

DATABASES = {

    #Configuração para POSTGRESQL COM VARIÁVEIS DE AMBIENTE
    # obs: caso tenha problemas com as variáveis de ambiente, trocar o acesso apara os.environ['DB_NAME']

    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': 5432,
    }

    # EXEMPLO COM SQLITE (nao precisa fazer setup de nenhum DB, nem de variaveis de ambiente)
    
    
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': os.path.join(BASE_DIR,'sqlite3.db')
    #}


}

# ATENÇÃO! 
# Alterar para um host valido,  '*' aceitará qualquer hostname
ALLOWED_HOSTS = ['*']






# Configurações adicionais de segurança, força HTTPS dentre outras coisas. Descomente-as para habilitar

# MIDDLEWARE += [
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'csp.middleware.CSPMiddleware',
# ]

# CSRF_COOKIE_SECURE = True
# CSRF_COOKIE_SAMESITE = 'Strict'
# SESSION_COOKIE_SECURE = True
# SECURE_BROWSER_XSS_FILTER = True
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_SSL_REDIRECT = True
# X_FRAME_OPTIONS = 'DENY'
# SECURE_HSTS_SECONDS = 15768001
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# CSP_DEFAULT_SRC = ("'none'",)
# CSP_STYLE_SRC = ("'self'",)
# CSP_SCRIPT_SRC = ("'self'",)
# CSP_FONT_SRC = ("'self'",)
# CSP_IMG_SRC = ("'self'",)