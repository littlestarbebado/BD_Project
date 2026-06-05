from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('clientes/', views.clientes_list_create, name='clientes_list_create'),
    path('ativos-tecnologicos/', views.ativos_list_create, name='ativos_list_create'),
    path('documentacao/', views.documentacao_list_create, name='documentacao_list_create'),
    path('incidentes/', views.incidentes_list_create, name='incidentes_list_create'),
    path('pedidos/', views.pedidos_list_create, name='pedidos_list_create'),
]
