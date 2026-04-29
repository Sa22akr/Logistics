import stripe
from decimal import Decimal

from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import Shipment
from .forms import ShipmentBookingForm


stripe.api_key = settings.STRIPE_SECRET_KEY


def home(request):
    return render(request, 'shipments/home.html')


def services(request):
    return render(request, 'shipments/services.html')


def careers(request):
    return render(request, 'shipments/careers.html')


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"Contact Form - {name}",
            message=f"From: {name}\nEmail: {email}\n\nMessage:\n{message}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
        )

    return render(request, 'shipments/contact.html')


def calculate_price(parcel_weight, delivery_option):
    weight = Decimal(str(parcel_weight or 1))

    if weight <= 1:
        base_price = Decimal("3.29")
    elif weight <= 2:
        base_price = Decimal("4.79")
    elif weight <= 5:
        base_price = Decimal("6.59")
    elif weight <= 10:
        base_price = Decimal("6.68")
    else:
        base_price = Decimal("10.28")

    if delivery_option == "Same Day":
        base_price += Decimal("7.00")
    elif delivery_option == "Next Day":
        base_price += Decimal("3.00")

    return base_price


def book_shipment(request):
    if request.method == "POST":
        form = ShipmentBookingForm(request.POST)

        if form.is_valid():
            shipment = form.save(commit=False)
            shipment.payment_status = "pending"
            shipment.status = "Pending Payment"
            shipment.price = calculate_price(
                shipment.parcel_weight,
                shipment.delivery_option
            )
            shipment.save()

            return redirect('booking_review', shipment_id=shipment.id)

    else:
        form = ShipmentBookingForm()

    return render(request, "shipments/book.html", {"form": form})


def booking_review(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    return render(request, 'shipments/booking_review.html', {
        'shipment': shipment
    })


def create_checkout_session(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        mode="payment",
        customer_email=shipment.sender_email,
        client_reference_id=str(shipment.id),
        line_items=[
            {
                "price_data": {
                    "currency": "gbp",
                    "product_data": {
                        "name": f"Civic Logistics Delivery - {shipment.tracking_number}",
                    },
                    "unit_amount": int(shipment.price * 100),
                },
                "quantity": 1,
            }
        ],
        success_url=f"{settings.SITE_URL}/booking-success/{shipment.id}/?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.SITE_URL}/booking-review/{shipment.id}/",
    )

    shipment.stripe_session_id = checkout_session.id
    shipment.save()

    return redirect(checkout_session.url)


def booking_success(request, shipment_id):
    shipment = get_object_or_404(Shipment, id=shipment_id)

    return render(request, "shipments/booking_success.html", {
        "shipment": shipment
    })


def track_shipment(request):
    shipment = None
    error = None

    if request.method == "POST":
        tracking_number = request.POST.get("tracking_number", "").strip().upper()

        try:
            shipment = Shipment.objects.get(tracking_number=tracking_number)
        except Shipment.DoesNotExist:
            error = "No shipment found with that tracking number."

    return render(request, "shipments/track.html", {
        "shipment": shipment,
        "error": error
    })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        shipment_id = session.get("client_reference_id")

        shipment = Shipment.objects.filter(id=shipment_id).first()

        if shipment:
            shipment.payment_status = "paid"
            shipment.status = "Booked"
            shipment.stripe_session_id = session.get("id")
            shipment.save()

    return HttpResponse(status=200)
