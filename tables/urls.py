from django.urls import path
from . import views

urlpatterns = [
    path('', views.tables_list, name='tables_list'),
    path('available/', views.available_tables, name='available_tables'),
]
