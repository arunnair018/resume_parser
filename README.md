# Django Setup + Project Structure Guide

This guide walks you through:
- Setting up Django using Miniconda
- Creating a project and app
- Understanding folder structure
- Explaining important Django files

---

# 1. Environment Setup (Miniconda)

## Create environment
```bash
conda create -n djangoenv python=3.12
````

## Activate environment

```bash
conda activate djangoenv
```

## Install Django

```bash
python -m pip install django
```

## Verify installation

```bash
python -m django --version
```

---

# 2. Create Django Project

## Create project

```bash
django-admin startproject myproject
cd myproject
```

## Run server

```bash
python manage.py runserver
```

Open:

```
http://127.0.0.1:8000/
```

---

# 3. Create an App

```bash
python manage.py startapp main
```

## Register app

In `myproject/settings.py`:

```python
INSTALLED_APPS = [
    ...
    'main',
]
```

---

# 4. Folder Structure Explained

After setup, your structure will look like:

```plaintext
myproject/
│
├── manage.py
│
├── myproject/        ← Project config folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── main/             ← Your app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── tests.py
    └── migrations/
```

---

# 5. Important Files Explained

## manage.py

```plaintext
Command-line utility for Django
```

Used for:

```bash
python manage.py runserver
python manage.py makemigrations
python manage.py migrate
```

---

## settings.py

```plaintext
Main configuration file
```

Contains:

* Installed apps
* Database config
* Templates config
* Static files config

Important section:

```python
INSTALLED_APPS = [
    'main',
]
```

---

## urls.py (Project level)

```plaintext
Main URL router
```

Example:

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("main.urls")),
]
```

👉 Connects app URLs to project

---

## views.py

```plaintext
Contains logic for each page
```

Example:

```python
from django.shortcuts import render

def home(request):
    return render(request, "main/index.html")
```

---

## models.py

```plaintext
Defines database structure
```

Example:

```python
from django.db import models

class Document(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

---

## admin.py

```plaintext
Registers models for admin panel
```

Example:

```python
from django.contrib import admin
from .models import Document

admin.site.register(Document)
```

---

## apps.py

```plaintext
App configuration
```

Usually no need to modify for beginners.

---

## migrations/

```plaintext
Tracks database changes
```

Auto-generated files when running:

```bash
python manage.py makemigrations
```

---

# 6. Adding URL Routing

## Create `main/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
]
```

---

## Connect to project

In `myproject/urls.py`:

```python
path("", include("main.urls")),
```

---

# 7. Templates Setup

## Folder structure

```plaintext
main/
└── templates/
    └── main/
        └── index.html
```

---

## Example template

```html
<!DOCTYPE html>
<html>
  <body>
    <h1>Hello Django</h1>
  </body>
</html>
```

---

## Render template

```python
return render(request, "main/index.html")
```

---

# 8. Database Setup

## Create model

```python
from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=100)
```

---

## Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

---

# 10. Core Django Flow

```plaintext
Request → URL → View → Template → Response
```

Example flow:

1. User visits `/`
2. URL routes to view
3. View processes logic
4. Template renders UI
5. Response sent back

---
