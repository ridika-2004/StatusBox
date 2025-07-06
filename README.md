# StatusBox

A small project to learn how to upload status with a text editor with django.

### Simplified Project Structure
```console
status_project/
│
├── posts/                
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/posts/
│       ├── create_post.html
│       └── home.html
│
├── status_project/      
│   ├── settings.py
│   └── urls.py
│
└── manage.py
```

## Guide

#### Install Packages
```console
pip install django django-ckeditor
```

#### Setup Django Project & App
Open terminal and write
```console
django-admin startproject status_project
cd status_project
python manage.py startapp posts
```

#### Configure `settings.py`
```python
INSTALLED_APPS = [
    ...
    'ckeditor',
    'posts',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
STATIC_URL = '/static/
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

#### Create Model in `posts/models.py`
```python
from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User

class StatusPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

#### Create Form in `posts/forms.py`
```python
from django import forms
from .models import StatusPost

class StatusPostForm(forms.ModelForm):
    class Meta:
        model = StatusPost
        fields = ['title', 'content']
```

#### Views in `posts/views.py`
```python
from django.shortcuts import render, redirect
from .forms import StatusPostForm
from .models import StatusPost
from django.contrib.auth.decorators import login_required

def home(request):
    posts = StatusPost.objects.all().order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = StatusPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = StatusPostForm()
    return render(request, 'posts/create_post.html', {'form': form})
```

#### URLs 
in `posts/urls.py`
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_post, name='create_post'),
]
```
In `status_project/urls.py`
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('posts.urls')),
]
```
#### In `posts/templates/posts`
create `create_post.html`
```html
{% extends 'posts/base.html' %}

{% block content %}
<h2>Create a New Status</h2>

<form method="POST">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit" class="button">Post</button>
</form>

<p><a href="{% url 'home' %}">← Back to Home</a></p>
{% endblock %}
```
create `base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Status App</title>
    <style>
        body { font-family: sans-serif; background: #f7f7f7; margin: 0; padding: 0; }
        header { background: #6200ea; color: white; padding: 10px 20px; }
        .container { max-width: 700px; margin: 20px auto; background: white; padding: 20px; border-radius: 5px; }
        a.button { background: #6200ea; color: white; padding: 8px 12px; text-decoration: none; border-radius: 4px; }
        .post { border-bottom: 1px solid #ddd; margin: 15px 0; padding-bottom: 10px; }
    </style>
</head>
<body>
    <header>
        <h1>Status App</h1>
    </header>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```
create `home.html`
```html
{% extends 'posts/base.html' %}

{% block content %}
<h2>Recent Posts</h2>
<p><a href="{% url 'create_post' %}" class="button">➕ Create New Post</a></p>

{% for post in posts %}
<div class="post">
    <h3>{{ post.title }}</h3>
    <small>by {{ post.author.username }} on {{ post.created_at }}</small>
    <div>{{ post.content|safe }}</div>
</div>
{% empty %}
<p>No posts yet.</p>
{% endfor %}
{% endblock %}
```
#### Run Collectstatic
```console
python manage.py collectstatic
```
#### Run & Test
```console
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

