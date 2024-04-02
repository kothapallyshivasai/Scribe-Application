from django.urls import path
from .views import history, home, validate_and_save, summary

urlpatterns = [
    path('', home, name="home"),
    path('validate_and_save', validate_and_save, name='validate_and_save'),
    path('summary', summary, name='summary'),
    path('history', history, name="history"),
]