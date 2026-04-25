from django import forms
from .models import Shipment


class ShipmentBookingForm(forms.ModelForm):
    class Meta:
        model = Shipment
        fields = [
            'sender_name',
            'sender_email',
            'sender_phone',
            'receiver_name',
            'receiver_phone',
            'pickup_address',
            'delivery_address',
            'parcel_size',
            'parcel_weight',
            'delivery_option',
        ]

        widgets = {
            'sender_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'sender_email': forms.EmailInput(attrs={'placeholder': 'Your email address'}),
            'sender_phone': forms.TextInput(attrs={'placeholder': 'Your phone number'}),

            'receiver_name': forms.TextInput(attrs={'placeholder': 'Receiver full name'}),
            'receiver_phone': forms.TextInput(attrs={'placeholder': 'Receiver phone number'}),

            'pickup_address': forms.Textarea(attrs={'placeholder': 'Pickup address', 'rows': 3}),
            'delivery_address': forms.Textarea(attrs={'placeholder': 'Delivery address', 'rows': 3}),

            'parcel_weight': forms.NumberInput(attrs={'placeholder': 'Weight in KG', 'step': '0.01'}),
        }