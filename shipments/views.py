from django.shortcuts import render, redirect
from .models import Shipment
from .forms import ShipmentBookingForm


def home(request):
    return render(request, 'shipments/home.html')


def track_shipment(request):
    shipment = None
    error = None

    if request.method == 'POST':
        tracking_number = request.POST.get('tracking_number', '').strip().upper()

        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
        except Shipment.DoesNotExist:
            error = "No shipment found with that tracking number."

    return render(request, 'shipments/track.html', {
        'shipment': shipment,
        'error': error
    })


def book_shipment(request):
    if request.method == 'POST':
        form = ShipmentBookingForm(request.POST)

        if form.is_valid():
            shipment = form.save()
            return redirect('booking_success', tracking_number=shipment.tracking_number)
    else:
        form = ShipmentBookingForm()

    return render(request, 'shipments/book.html', {'form': form})


def booking_success(request, tracking_number):
    shipment = Shipment.objects.get(tracking_number=tracking_number)

    return render(request, 'shipments/booking_success.html', {
        'shipment': shipment
    })