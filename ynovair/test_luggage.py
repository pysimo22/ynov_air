#!/usr/bin/env python
"""
Integration test for the luggage settings functionality
Tests model creation, calculations, and data integrity
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from django.test import TestCase
from django.contrib.auth.models import User
from flights.models import Airport, Flight, Passenger, Booking, Baggage, LuggageSettings
from datetime import datetime, timedelta
from decimal import Decimal

def test_luggage_functionality():
    """Test complete luggage functionality"""
    
    print("=" * 70)
    print("LUGGAGE SETTINGS FUNCTIONALITY TEST")
    print("=" * 70)
    
    # Test 1: LuggageSettings model
    print("\n[TEST 1] LuggageSettings Model")
    print("-" * 70)
    try:
        luggage_settings = LuggageSettings.objects.filter(is_active=True).first()
        assert luggage_settings is not None, "LuggageSettings not found"
        assert luggage_settings.free_baggage_allowance == Decimal('20'), "Free allowance mismatch"
        assert luggage_settings.price_per_extra_kg == Decimal('5'), "Price mismatch"
        print("✓ LuggageSettings loaded successfully")
        print(f"  - Free baggage allowance: {luggage_settings.free_baggage_allowance} kg")
        print(f"  - Max baggage per item: {luggage_settings.max_baggage_per_item} kg")
        print(f"  - Price per extra kg: {luggage_settings.price_per_extra_kg} €")
    except Exception as e:
        print(f"✗ LuggageSettings test failed: {e}")
        return False
    
    # Test 2: Create test data
    print("\n[TEST 2] Creating Test Data")
    print("-" * 70)
    try:
        # Create or get airports
        origin, _ = Airport.objects.get_or_create(
            code="CDG",
            defaults={
                "name": "Charles de Gaulle",
                "city": "Paris",
                "country": "France"
            }
        )
        destination, _ = Airport.objects.get_or_create(
            code="JFK",
            defaults={
                "name": "John F. Kennedy",
                "city": "New York",
                "country": "USA"
            }
        )
        
        # Create flight
        departure = datetime.now() + timedelta(days=7)
        arrival = departure + timedelta(hours=8)
        flight, _ = Flight.objects.get_or_create(
            flight_number="AF100TEST",
            defaults={
                "origin": origin,
                "destination": destination,
                "departure_time": departure,
                "arrival_time": arrival,
                "duration": timedelta(hours=8),
                "available_seats": 100,
                "total_seats": 100,
                "price": Decimal('150.00'),
                "status": 'SCHEDULED'
            }
        )
        
        # Create passenger
        passenger, _ = Passenger.objects.get_or_create(
            passport_number="AB123456TEST",
            defaults={
                "first_name": "Jean",
                "last_name": "Dupont",
                "email": "jean@example.com",
                "phone": "+33612345678",
                "date_of_birth": "1990-01-15"
            }
        )
        
        # Create user
        user, _ = User.objects.get_or_create(
            username="testuser",
            defaults={
                "email": "test@example.com"
            }
        )
        if not user.check_password("testpass123"):
            user.set_password("testpass123")
            user.save()
        
        # Create booking
        booking, _ = Booking.objects.get_or_create(
            booking_reference="TEST1001",
            defaults={
                "flight": flight,
                "passenger": passenger,
                "user": user,
                "number_of_passengers": 1,
                "total_price": Decimal('150.00'),
                "status": 'CONFIRMED'
            }
        )
        
        print("✓ Test data created successfully")
        print(f"  - Flight: {flight.flight_number} ({origin.code} → {destination.code})")
        print(f"  - Passenger: {passenger.get_full_name()}")
        print(f"  - Booking: {booking.booking_reference}")
    except Exception as e:
        print(f"✗ Data creation failed: {e}")
        return False
    
    # Test 3: Baggage creation and calculations
    print("\n[TEST 3] Baggage Creation and Calculations")
    print("-" * 70)
    try:
        # Clear existing baggages for this booking
        booking.baggages.all().delete()
        
        # Create baggage within allowance
        baggage1, _ = Baggage.objects.get_or_create(
            booking=booking,
            weight_kg=Decimal('18.5'),
            defaults={
                "quantity": 1,
                "description": "Valise noire",
                "status": 'REGISTERED',
                "is_extra": False
            }
        )
        
        # Create baggage exceeding allowance
        baggage2, _ = Baggage.objects.get_or_create(
            booking=booking,
            weight_kg=Decimal('28.0'),
            defaults={
                "quantity": 1,
                "description": "Sac à dos gris",
                "status": 'REGISTERED',
                "is_extra": True
            }
        )
        
        print("✓ Baggage objects created successfully")
        
        # Test excess weight calculation
        excess_weight = baggage2.get_excess_weight()
        expected_excess = Decimal('8.0')  # 28 - 20
        assert excess_weight == expected_excess, f"Excess weight mismatch: {excess_weight} != {expected_excess}"
        print(f"  - Baggage 1 (18.5 kg): Within allowance ✓")
        print(f"  - Baggage 2 (28.0 kg): Excess weight = {excess_weight} kg ✓")
        
        # Test extra charge calculation
        extra_charge = baggage2.calculate_extra_charge()
        expected_charge = expected_excess * luggage_settings.price_per_extra_kg
        assert extra_charge == expected_charge, f"Extra charge mismatch: {extra_charge} != {expected_charge}"
        print(f"  - Extra charge for Baggage 2: {extra_charge} € ✓")
        
    except Exception as e:
        print(f"✗ Baggage test failed: {e}")
        return False
    
    # Test 4: Booking total with luggage charges
    print("\n[TEST 4] Booking Total with Luggage Charges")
    print("-" * 70)
    try:
        # Update booking with luggage charges
        total_excess_charge = Decimal('0')
        for baggage in booking.baggages.all():
            total_excess_charge += baggage.calculate_extra_charge()
        
        booking.total_price = flight.price + total_excess_charge
        booking.save()
        
        expected_total = Decimal('150.00') + Decimal('40.00')  # Flight + (8kg * 5€)
        assert booking.total_price == expected_total, f"Booking total mismatch: {booking.total_price} != {expected_total}"
        print(f"  - Flight price: {flight.price} €")
        print(f"  - Luggage charges: {total_excess_charge} €")
        print(f"  - Total: {booking.total_price} € ✓")
        
    except Exception as e:
        print(f"✗ Booking total test failed: {e}")
        return False
    
    # Test 5: Admin registration
    print("\n[TEST 5] Admin Registration")
    print("-" * 70)
    try:
        from django.contrib.admin.sites import site
        models = list(site._registry.keys())
        model_names = [m.__name__ for m in models]
        
        required_models = ['LuggageSettings', 'Baggage']
        for model in required_models:
            assert model in model_names, f"{model} not registered in admin"
        
        print("✓ All models registered in admin")
        print(f"  - LuggageSettings: Registered ✓")
        print(f"  - Baggage: Enhanced with new fields ✓")
        
    except Exception as e:
        print(f"✗ Admin registration test failed: {e}")
        return False
    
    print("\n" + "=" * 70)
    print("ALL TESTS PASSED ✓")
    print("=" * 70)
    return True

if __name__ == '__main__':
    success = test_luggage_functionality()
    exit(0 if success else 1)
