from django.shortcuts import render
from .models import Shipment

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