# Django App - MAC

Uso básico de django en un ambiente virtual con conexión a una DB y URLs asignados 

## Descripción

El proyecto muestra el uso y configuración de una aplicación básica de django que se puede ver en el localhost y permite la creación, visualización y edición de archivos por medio de URLs asignados donde los archivos generados se almacenan en una base de datos mysql.
Igualmente aqui se encuentra el step by step de como llegar al mismo resultado.


### Virtual Env

Para poder inicializar un Virtual Env debemos estar dentro de la carpeta designada para el proyecto y escribir el siguiente comando 
```
virtualenv env --python=3.13
```
Esta parte simplemente fue la creación del ambiente, para poder trabajar dentro del mismo debemos activarlo 
```
source ./env/bin/activate
```

### Django

Ahora es momento de instalar Django                                              
```
pip install django
```

Creamos un nuevo proyecto, en este caso article_manager 
```
django-admin startproject article_manager   
```

Después vamos a revisar las migraciones pendientes y en caso de tenerlas, le pediremos a django que las haga
``` 
python manage.py showmigrations
python manage.py migrate
```

Y listo, ya tenemos Django y podemos comprobando con el siguiente comando y entrando a 0.0.0.0:8000 en nuestro buscador
```
python manage.py runserver 0.0.0.0:8000  
```

Es posible que aparezca un error mencionando a los ALLOWED-HOSTS, en ese caso debemos entrar a al archivo settings.py en 
article_manager/settings.py y una vez dentro, en la linea 28 vamos a agregar 0.0.0.0 como ALLOWED-HOSTS
ALLOWED_HOSTS = ['0.0.0.0']
Después de editar esto podemos entrar http://0.0.0.0:8000/ en el buscador y veremos el cohete despegando de django

Una vez confirmado que se puede ver la pantalla mencionada, vamos a crear nuestro superuser y seguiremos las instrucciones
```
python manage.py createsuperuser
```
Ahora entramos a http://0.0.0.0:8000/admin/ y vamos a ingresar el usuario y contraseñas recien generados


### Mysql

Para este proyecto vamos a usar Mysql por lo que lo vamos a habilitar la base de datos 
```
 mysql -u tuUsuario -p tuContraseña
```
una vez dentro, creamos la DB que vamos a usar 
```
CREATE DATABASE article_manager
```
y listo, de parte de Mysql ya quedo, el resto de configuraciones van en los archivos creados previamente por django


### Settings

Nuevamente vamos a ir a article_manager/settings.py a editar la parte de la DB
Cambiaremos 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

por 

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'article_manager',
        'USER': 'tuUser',
        'PASSWORD': 'tuContraseña',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

Con esto ya tenemos habilitada nuestra DB con django


## App

Hasta ahora solo hemos creado el ambiente virtual, instalado librerias y habilitar una DB, falta crear la aplicación
```
python manage.py startapp articles
```
Ahora debemos volver a article_manager/settings.py a agregar el nombre de nuestra app de la siguiente manera 
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'articles', 

]

## Estructura
Hasta ahora debemos tener tres carpetas 
- article_manager (proyecto)
- articles (app)
- env (Ambiente virtual)

Pero dentro de estas tenemos archivos importantes, los que vamos a modificar posteriormente son
- article_manager/settings.py
- article_manager/urls.py

- articles/admin.py
- articles/models.py
- articles/views.py

Además vamos a agregar los siguientes archivos 
- articles/forms.py
- articles/urls.py

Y el siguiente folder con sus archivos 
- articles/templates
- articles/templates/articles
  
- articles/templates/article_template.html
- articles/templates/edit_article_form.html
- articles/templates/new_article_form.html

- articles/templates/articles/article_detail.html
- articles/templates/articles/article_list.html

## Ediciones a archivos 

En article_manager/urls.py agregaremos los urls creados en articles 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('articles/', include('articles.urls')),
]

En articles/models.py crearemos la clase Archivo que tendra un nombre y un contenido
class Article(models.Model):
    name = models.CharField("Nombre" , default="Sin nombre", null= False, max_length=200)
    content = models.TextField("Contenido", default="", blank=True)

    def __str__(self):
        return self.name

En articles/admin.py registraremos el Articulo recien creado
from django.contrib import admin
from .models import Article
admin.site.register(Article)


En articles/forms.py a partir de ModelForm crearemos la clase de ArticleForm
from django.forms import ModelForm
from .models import Article
class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['name', 'content']

## URLs
Usaremos en este caso el ejemplo de mostrar todas las entidades guardadas hasta el momento y la creacion de una nueva entidad

En articles/views.py la vista que nos muestra todos los documentos es
    
class ArticleListView(ListView): 
    model = Article
    context_object_name = 'articlesList'

Y la que nos permite generar una nueva entidad es
        
class NewArticleForm(View):
    def get(self, request):
        form = ArticleForm(
)        return render(request, 'new_article_form.html', {'form': form})

    def post(self, request):
        form = ArticleForm(request.POST)
            
        if form.is_valid():
            form.save()
            return redirect('all_articles')
        return render(request, 'new_article_form.html', {'form': form})

Ahora en articles/templates/articles/article_list.html escribimos
{% block content %}
    <h2>Article</h2>
    <ul>
        {% for article in articlesList %}
            <li>{{ article.name }}</li>
        {% endfor %}
    </ul>
{% endblock %}

y en articles/templates/new_article_form.html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Create Article</button>
</form>

Ahora solo nos falta agregar la URL en articles/urls.py que usaremos
from django.urls import path
from . import views


urlpatterns = [
    path('', views.ArticleView.as_view(), name='article_list'),
    path('all', views.ArticleListView.as_view(), name='all_articles'),
    path('new', views.NewArticleForm.as_view(), name='new_article'),
]




## Acknowledgments

Documentación sobre tecnologias usadas
* [Django](https://docs.djangoproject.com/en/6.0/intro/tutorial01/)
* [Mysql](https://formulae.brew.sh/formula/mysql)
