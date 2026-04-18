
from django.urls import path
from .views import home, upload_resume


urlpatterns = [
    path('', home, name='home'),
    path('upload/', upload_resume, name='upload_resume'),
]