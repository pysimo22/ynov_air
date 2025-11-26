#!/usr/bin/env python
"""
Test script to diagnose booking creation issues
"""
import os
import django
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from flights.models import Flight, Passenger, Booking, Baggage, Airport
from django.contrib.auth.models import User
from datetime import datetime, timedelta

print("=" * 60)
print("BOOKING CREATION TEST")
print("=" * 60)

try:
    # Get test data
    flight = Flight.objects.first()
    user = User.objects.filter(is_staff=False).first()
    
    if not flight:
        print("❌ ERROR: No flights found in database")
        exit(1)
    
    if not user:
        print("❌ ERROR: No users found in database")
        exit(1)
    
    print(f"✓ Flight found: {flight.flight_number}")
    print(f"✓ User found: {user.username}")
    print(f"✓ Flight price: {flight.price}€")
    print(f"✓ Available seats: {flight.available_seats}")
    
    # Create a test passenger
    passenger_data = {
        'first_name': 'Test',
        'last_name': 'Passenger',
        'email': f'test{Booking.objects.count()}@test.com',
        'phone': '0123456789',
        'passport_number': f'TESTPASS{Booking.objects.count()}',
        'date_of_birth': datetime.now().date() - timedelta(days=365*25),
    }
    
    passenger = Passenger.objects.create(**passenger_data)
    print(f"✓ Passenger created: {passenger.first_name} {passenger.last_name}")
    
    # Try to create booking
    booking_ref = f"TEST{Booking.objects.count():05d}"
    booking = Booking.objects.create(
        booking_reference=booking_ref,
        flight=flight,
        passenger=passenger,
        user=user,
        number_of_passengers=1,
        total_price=Decimal(flight.price),
        status='CONFIRMED'
    )
    print(f"✓ Booking created: {booking.booking_reference}")
    print(f"✓ Booking ID: {booking.id}")
    
    # Try to create baggage
    baggage = Baggage.objects.create(
        booking=booking,
        weight_kg=Decimal('20.50'),
        status='REGISTERED'
    )
    print(f"✓ Baggage created: {baggage.id}")
    
    print("\n" + "=" * 60)
    print("✅ BOOKING TEST SUCCESSFUL!")
    print("=" * 60)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
