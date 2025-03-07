from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseBadRequest, HttpResponseNotAllowed
from .models import Reservation
from customers.models import Customer
from tables.models import Table
from datetime import datetime

def reservations_list(request):
    """
    Вывод списка всех бронирований с возможностью выбора клиентов и столиков.
    """
    reservations = Reservation.objects.all().order_by('-date')  # Сортируем по дате (сначала новые)
    customers = Customer.objects.all()
    tables = Table.objects.all()
    
    return render(request, 'reservations/reservations_list.html', {
        'reservations': reservations,
        'customers': customers,
        'tables': tables
    })

def create_reservation(request):
    """
    Создание бронирования через форму на сайте.
    """
    if request.method == 'POST':
        customer_id = request.POST.get('customer_id')
        table_id = request.POST.get('table_id')
        date_str = request.POST.get('date')

        # Проверяем, что все поля заполнены
        if not customer_id or not table_id or not date_str:
            return HttpResponseBadRequest("Заполните все поля!")

        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return HttpResponseBadRequest("Неверный формат даты. Используйте YYYY-MM-DD.")

        # Проверяем, существует ли клиент и столик
        customer = Customer.objects.filter(pk=customer_id).first()
        table = Table.objects.filter(pk=table_id).first()

        if not customer or not table:
            return HttpResponseBadRequest("Клиент или столик не найден.")

        # Проверяем, свободен ли столик на указанную дату
        if Reservation.objects.filter(table=table, date=date_obj).exists():
            return HttpResponseBadRequest("Этот столик уже забронирован на данную дату.")

        # Проверяем, что у пользователя нет другого бронирования на этот день
        if Reservation.objects.filter(customer=customer, date=date_obj).exists():
            return HttpResponseBadRequest("У вас уже есть бронь на эту дату.")

        # Создаем новую бронь
        Reservation.objects.create(customer=customer, table=table, date=date_obj, status='pending')

        return redirect('reservations_list')

    return HttpResponseNotAllowed(['POST'])

def reservation_detail(request, id):
    """
    Просмотр конкретного бронирования.
    """
    reservation = get_object_or_404(Reservation, pk=id)
    return render(request, 'reservations/reservation_detail.html', {'reservation': reservation})

def update_reservation_status(request, id):
    """
    Обновление статуса бронирования.
    """
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=id)
        new_status = request.POST.get('status')

        if new_status not in dict(Reservation.STATUS_CHOICES):
            return HttpResponseBadRequest("Неверный статус!")

        reservation.status = new_status
        reservation.save()
        return redirect('reservations_list')

    return HttpResponseNotAllowed(['POST'])

def delete_reservation(request, id):
    """
    Удаление бронирования.
    """
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, pk=id)
        reservation.delete()
        return redirect('reservations_list')

    return HttpResponseNotAllowed(['POST'])

def user_reservations(request, user_id):
    """
    Отображение всех бронирований конкретного пользователя.
    """
    reservations = Reservation.objects.filter(customer__id=user_id).order_by('-date')
    return render(request, 'reservations/reservations_list.html', {'reservations': reservations})
