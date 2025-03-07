from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')  # Отображаем шаблон home.html

urlpatterns = [
    path('', home, name='home'),  # Добавляем этот маршрут для главной страницы
    path('admin/', admin.site.urls),
    path('customers/', include('customers.urls')),
    path('tables/', include('tables.urls')),
    path('reservations/', include('reservations.urls')),
]
