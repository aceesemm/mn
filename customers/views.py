from django.shortcuts import render, get_object_or_404
from .models import Customer
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import json

def customers_list(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        return render(request, 'customers/customers_list.html', {'customers': customers})
    elif request.method == 'POST':
        data = json.loads(request.body)
        name = data.get('name')
        phone = data.get('phone')
        if not name or not phone:
            return HttpResponseBadRequest("Отсутствуют необходимые поля")
        customer = Customer.objects.create(name=name, phone=phone)
        return JsonResponse({'id': customer.id, 'name': customer.name, 'phone': customer.phone})
        
def customer_detail(request, id):
    customer = get_object_or_404(Customer, pk=id)
    if request.method == 'GET':
        return render(request, 'customers/customer_detail.html', {'customer': customer})
