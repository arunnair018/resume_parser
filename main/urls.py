
from django.urls import path
from .views import home, parsed_resume


urlpatterns = [
    path('', home, name='home'),
    path('transcript/', parsed_resume, name='parsed_resume'),
]