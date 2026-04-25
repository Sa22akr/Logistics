from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('track/', views.track_shipment, name='track_shipment'),
    path('book/', views.book_shipment, name='book_shipment'),
    path('booking-success/<str:tracking_number>/', views.booking_success, name='booking_success'),
]