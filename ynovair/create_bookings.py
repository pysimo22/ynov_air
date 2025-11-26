import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from flights.models import Booking, Flight, Passenger, Airport
from django.contrib.auth.models import User
from decimal import Decimal
import random
import string

try:
    # Créer ou obtenir 2 aéroports
    cdg, _ = Airport.objects.get_or_create(
        code='CDG',
        defaults={'name': 'Charles de Gaulle', 'city': 'Paris', 'country': 'France'}
    )
    lhr, _ = Airport.objects.get_or_create(
        code='LHR',
        defaults={'name': 'London Heathrow', 'city': 'London', 'country': 'UK'}
    )
    
    # Créer 5 vols
    flights = []
    for i in range(1, 6):
        flight, _ = Flight.objects.get_or_create(
            flight_number=f'AF{i:03d}',
            defaults={
                'origin': cdg,
                'destination': lhr,
                'departure_time': '2025-11-25 10:00:00',
                'arrival_time': '2025-11-25 12:00:00',
                'duration': '02:00:00',
                'available_seats': 250,
                'total_seats': 300,
                'price': Decimal('150.00'),
                'status': 'SCHEDULED'
            }
        )
        flights.append(flight)
    
    print(f"✓ {len(flights)} vols créés/vérifiés")
    
    # Créer 10 passagers
    passengers = []
    for i in range(1, 11):
        passenger, _ = Passenger.objects.get_or_create(
            passport_number=f'PP{i:06d}',
            defaults={
                'first_name': f'Passager{i}',
                'last_name': f'Test{i}',
                'email': f'pass{i}@example.com',
                'phone': f'0612345{i:03d}',
                'date_of_birth': '1990-01-01'
            }
        )
        passengers.append(passenger)
    
    print(f"✓ {len(passengers)} passagers créés/vérifiés")
    
    # Créer 2 utilisateurs
    users = []
    for i in range(1, 3):
        user, _ = User.objects.get_or_create(
            username=f'user{i}',
            defaults={'email': f'user{i}@example.com'}
        )
        users.append(user)
    
    print(f"✓ {len(users)} utilisateurs créés/vérifiés")
    
    # Créer 30 nouvelles réservations
    statuses = ['PENDING', 'CONFIRMED', 'CHECKED_IN', 'CANCELLED']
    created_count = 0
    
    for i in range(30):
        ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        booking = Booking.objects.create(
            booking_reference=ref,
            flight=random.choice(flights),
            passenger=random.choice(passengers),
            number_of_passengers=random.randint(1, 4),
            total_price=Decimal(random.randint(200, 2000)) + Decimal('.99'),
            status=random.choice(statuses),
            seat_number=f'{random.randint(1, 30):02d}{random.choice("ABCDEF")}' if random.random() > 0.3 else None,
            user=random.choice(users + [None])
        )
        created_count += 1
    
    print(f"\n✅ {created_count} nouvelles réservations créées avec succès!")
    print(f"Total réservations: {Booking.objects.count()}")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
