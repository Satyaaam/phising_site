# phishing_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('check-phishing/', views.check_phishing, name='check_phishing'),
    # path('hello/', views.helloname)
]
