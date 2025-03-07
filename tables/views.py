from django.shortcuts import render, get_object_or_404
from .models import Table
from django.http import JsonResponse, HttpResponseBadRequest
import json
from datetime import datetime

def tables_list(request):
    if request.method == 'GET':
        tables = Table.objects.all()
        return render(request, 'tables/tables_list.html', {'tables': tables})
    elif request.method == 'POST':
        data = json.loads(request.body)
        number = data.get('number')
        seats = data.get('seats')
        if number is None or seats is None:
            return HttpResponseBadRequest("Отсутствуют необходимые поля")
        try:
            table = Table.objects.create(number=number, seats=seats)
        except Exception as e:
            return HttpResponseBadRequest(str(e))
        return JsonResponse({
            'id': table.id,
            'number': table.number,
            'seats': table.seats,
            'is_available': table.is_available
        })
        
def available_tables(request):
    # Ожидаем параметр GET 'date' в формате YYYY-MM-DD
    date_str = request.GET.get('date')
    if not date_str:
        return HttpResponseBadRequest("Параметр date обязателен")
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponseBadRequest("Неверный формат даты. Используйте YYYY-MM-DD")
    
    # Здесь для простоты полагаем, что доступность хранится в модели Table
    tables = Table.objects.filter(is_available=True)
    return render(request, 'tables/available_tables.html', {'tables': tables, 'date': date_obj})
