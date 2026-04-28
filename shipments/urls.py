from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    path('track/', views.track_shipment, name='track_shipment'),
    path('book/', views.book_shipment, name='book_shipment'),
    path('careers/', views.careers, name='careers'),
]