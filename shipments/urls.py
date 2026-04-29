from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),

    path('services/', views.services, name='services'),
    path('contact/', views.contact, name='contact'),

    path('track/', views.track_shipment, name='track_shipment'),
    path('book/', views.book_shipment, name='book_shipment'),
    path('careers/', views.careers, name='careers'),
    path("booking-success/<int:shipment_id>/", views.booking_success, name="booking_success"),
    path("stripe/webhook/", views.stripe_webhook, name="stripe_webhook"),
    path("booking-review/<int:shipment_id>/", views.booking_review, name="booking_review"),
    path("create-checkout-session/<int:shipment_id>/", views.create_checkout_session, name="create_checkout_session"),
]