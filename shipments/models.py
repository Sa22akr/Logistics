from django.db import models
import random
import string


def generate_tracking_number():
    return "CL" + ''.join(random.choices(string.digits, k=8))


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('Pending Payment', 'Pending Payment'),
        ('Booked', 'Booked'),
        ('Collected', 'Collected'),
        ('In Transit', 'In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]

    PARCEL_SIZE_CHOICES = [
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
        ('Extra Large', 'Extra Large'),
    ]

    DELIVERY_OPTION_CHOICES = [
        ('Standard', 'Standard Delivery'),
        ('Next Day', 'Next Day Delivery'),
        ('Same Day', 'Same Day Delivery'),
    ]

    tracking_number = models.CharField(
        max_length=20,
        unique=True,
        default=generate_tracking_number
    )

    sender_name = models.CharField(max_length=100)
    sender_email = models.EmailField()
    sender_phone = models.CharField(max_length=20)

    receiver_name = models.CharField(max_length=100)
    receiver_phone = models.CharField(max_length=20)

    pickup_address = models.TextField()
    delivery_address = models.TextField()

    parcel_size = models.CharField(max_length=20, choices=PARCEL_SIZE_CHOICES)
    parcel_weight = models.DecimalField(max_digits=6, decimal_places=2, help_text="Weight in KG")

    delivery_option = models.CharField(max_length=20, choices=DELIVERY_OPTION_CHOICES)

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Pending Payment'
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )

    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)

    stripe_session_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number