from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_validacion, name='initial_form'),
    path('preguntas/', views.vista_preguntas, name='titularidad'),
    path('export/', views.export_records, name='export_records'),
]