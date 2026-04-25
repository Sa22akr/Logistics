from django.db import models
import random
import string


def generate_tracking_number():
    return "CL" + ''.join(random.choices(string.digits, k=8))


class Shipment(models.Model):
    STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Collected', 'Collected'),
        ('In Transit', 'In Transit'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    tracking_number = models.CharField(
        max_length=20,
        unique=True,
        default=generate_tracking_number
    )

    sender_name = models.CharField(max_length=100)
    receiver_name = models.CharField(max_length=100)
    pickup_address = models.TextField()
    delivery_address = models.TextField()

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='Booked'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tracking_number