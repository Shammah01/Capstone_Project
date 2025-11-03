from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment, name='book_appointment'),
    path('list/', views.appointment_list, name='appointment_list'),
    path('<int:pk>/cancel/', views.cancel_appointment, name='cancel_appointment'),
]
