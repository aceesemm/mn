from django.urls import path
from .views import reservations_list, create_reservation, reservation_detail, update_reservation_status, delete_reservation, user_reservations

urlpatterns = [
    path('', reservations_list, name='reservations_list'),
    path('create/', create_reservation, name='create_reservation'),
    path('<int:id>/', reservation_detail, name='reservation_detail'),
    path('<int:id>/update/', update_reservation_status, name='update_reservation_status'),
    path('<int:id>/delete/', delete_reservation, name='delete_reservation'),
    path('user/<int:user_id>/', user_reservations, name='user_reservations'),
]
