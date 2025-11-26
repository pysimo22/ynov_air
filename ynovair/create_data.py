import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from django.contrib.auth.models import User
from flights.models import Airport, Flight, Passenger, Booking
from datetime import datetime, timedelta
from decimal import Decimal
import random
import string

# Create superuser
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print("✓ Superuser created")

# Create regular users
for i in range(1, 3):
    User.objects.get_or_create(username=f'user{i}', defaults={'email': f'user{i}@example.com'})
print("✓ Users created")

# Create airports
airports_data = [
    {'code': 'CDG', 'name': 'Charles de Gaulle', 'city': 'Paris', 'country': 'France'},
    {'code': 'ORY', 'name': 'Orly', 'city': 'Paris', 'country': 'France'},
    {'code': 'LHR', 'name': 'London Heathrow', 'city': 'London', 'country': 'UK'},
    {'code': 'AMS', 'name': 'Amsterdam', 'city': 'Amsterdam', 'country': 'Netherlands'},
]
for airport in airports_data:
    Airport.objects.get_or_create(code=airport['code'], defaults=airport)
print("✓ Airports created")

# Create flights
airports_list = list(Airport.objects.all())[:2]
base_time = datetime.now()

for i in range(1, 51):
    Flight.objects.create(
        flight_number=f'AF{i:04d}',
        origin=airports_list[0],
        destination=airports_list[1],
        departure_time=base_time + timedelta(days=i % 30),
        arrival_time=base_time + timedelta(days=i % 30, hours=2),
        duration=timedelta(hours=2),
        available_seats=200,
        total_seats=300,
        price=Decimal('150.00'),
        status='SCHEDULED'
    )
print("✓ Flights created")

# Create passengers
for i in range(1, 51):
    Passenger.objects.create(
        first_name=f'Passager{i}',
        last_name=f'Last{i}',
        email=f'passenger{i}@example.com',
        phone=f'0612345{i:03d}',
        passport_number=f'PP{i:06d}',
        date_of_birth='1990-01-01'
    )
print("✓ Passengers created")

# Create 30 bookings
statuses = ['PENDING', 'CONFIRMED', 'CANCELLED', 'CHECKED_IN']
users = list(User.objects.filter(username__startswith='user'))
flights = list(Flight.objects.all())[:30]
passengers = list(Passenger.objects.all())[:30]

for i in range(30):
    booking_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    Booking.objects.create(
        booking_reference=booking_ref,
        flight=flights[i],
        passenger=passengers[i],
        user=random.choice(users) if users else None,
        number_of_passengers=random.randint(1, 5),
        total_price=Decimal(str(random.randint(200, 2000) + random.random())),
        status=random.choice(statuses)
    )

print(f"✓ 30 Bookings created")
print("\n✅ All data created successfully!")
print("=" * 50)
print("Admin credentials: admin / admin")
print("=" * 50)
