#!/usr/bin/env python
"""
Generate 50 rows of sample data for each model in YnovAir database
Run with: python generate_50_rows.py
"""

import os
import django
from datetime import datetime, timedelta
from decimal import Decimal
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from django.contrib.auth.models import User
from flights.models import Airport, Flight, Passenger, Booking, Baggage

def clear_data():
    """Clear existing data"""
    print("🗑️  Clearing existing data...")
    Baggage.objects.all().delete()
    Booking.objects.all().delete()
    Flight.objects.all().delete()
    Passenger.objects.all().delete()
    Airport.objects.all().delete()
    User.objects.filter(username__startswith='user').delete()
    print("✓ Data cleared")

def create_users():
    """Create 50 users"""
    print("\n👥 Creating 50 users...")
    users = []
    for i in range(1, 51):
        user, created = User.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'first_name': f'User',
                'last_name': f'Number{i}',
            }
        )
        if created:
            user.set_password('password123')
            user.save()
        users.append(user)
    print(f"✓ {len(users)} users created")
    return users

def create_airports():
    """Create 50 airports"""
    print("\n✈️  Creating 50 airports...")
    
    airport_data = [
        ('CDG', 'Paris Charles de Gaulle', 'Paris', 'France'),
        ('ORY', 'Paris Orly', 'Paris', 'France'),
        ('LHR', 'London Heathrow', 'London', 'UK'),
        ('LGW', 'London Gatwick', 'London', 'UK'),
        ('AMS', 'Amsterdam Schiphol', 'Amsterdam', 'Netherlands'),
        ('DUB', 'Dublin Airport', 'Dublin', 'Ireland'),
        ('BCN', 'Barcelona El Prat', 'Barcelona', 'Spain'),
        ('MAD', 'Madrid Barajas', 'Madrid', 'Spain'),
        ('MUC', 'Munich Franz Josef Strauss', 'Munich', 'Germany'),
        ('BER', 'Berlin Brandenburg', 'Berlin', 'Germany'),
        ('ZRH', 'Zurich Airport', 'Zurich', 'Switzerland'),
        ('VIE', 'Vienna International', 'Vienna', 'Austria'),
        ('CPH', 'Copenhagen Kastrup', 'Copenhagen', 'Denmark'),
        ('ARN', 'Stockholm Arlanda', 'Stockholm', 'Sweden'),
        ('OSL', 'Oslo Gardermoen', 'Oslo', 'Norway'),
        ('HEL', 'Helsinki Vantaa', 'Helsinki', 'Finland'),
        ('WAW', 'Warsaw Chopin', 'Warsaw', 'Poland'),
        ('PRG', 'Prague Václav Havel', 'Prague', 'Czech Republic'),
        ('BUD', 'Budapest Ferenc Liszt', 'Budapest', 'Hungary'),
        ('BRU', 'Brussels Zaventem', 'Brussels', 'Belgium'),
    ]
    
    airports = []
    for i in range(50):
        if i < len(airport_data):
            code, name, city, country = airport_data[i]
        else:
            code = f'AP{i:02d}'
            name = f'Airport {i}'
            city = f'City {i}'
            country = f'Country {i}'
        
        airport, created = Airport.objects.get_or_create(
            code=code,
            defaults={
                'name': name,
                'city': city,
                'country': country,
            }
        )
        airports.append(airport)
    
    print(f"✓ {len(airports)} airports created")
    return airports

def create_flights(airports):
    """Create 50 flights"""
    print("\n🛫 Creating 50 flights...")
    
    flights = []
    airlines = ['AF', 'BA', 'LH', 'KL', 'IB', 'SQ', 'UA', 'DL']
    
    for i in range(1, 51):
        airline = random.choice(airlines)
        flight_number = f'{airline}{i:04d}'
        
        origin = random.choice(airports)
        destination = random.choice([a for a in airports if a != origin])
        
        departure_time = datetime.now() + timedelta(days=random.randint(1, 30), hours=random.randint(0, 23))
        duration_hours = random.randint(1, 12)
        arrival_time = departure_time + timedelta(hours=duration_hours)
        
        flight, created = Flight.objects.get_or_create(
            flight_number=flight_number,
            defaults={
                'origin': origin,
                'destination': destination,
                'departure_time': departure_time,
                'arrival_time': arrival_time,
                'duration': timedelta(hours=duration_hours),
                'total_seats': random.randint(100, 400),
                'available_seats': random.randint(10, 100),
                'price': Decimal(str(round(random.uniform(50, 500), 2))),
                'status': 'SCHEDULED',
            }
        )
        flights.append(flight)
    
    print(f"✓ {len(flights)} flights created")
    return flights

def create_passengers():
    """Create 50 passengers"""
    print("\n👨‍✈️ Creating 50 passengers...")
    
    first_names = ['Jean', 'Marie', 'Pierre', 'Sophie', 'Luc', 'Anne', 'Marc', 'Julie', 'Paul', 'Claire',
                   'Thomas', 'Amélie', 'Nicolas', 'Camille', 'Alexandre', 'Isabelle', 'François', 'Laurence',
                   'Louis', 'Nathalie', 'Charles', 'Valérie', 'Laurent', 'Stéphanie', 'Michel', 'Dominique',
                   'Joseph', 'Christine', 'Bernard', 'Catherine', 'Jacques', 'Monique', 'Robert', 'Martine',
                   'Philippe', 'Francine', 'André', 'Danielle', 'Henri', 'Josée']
    
    last_names = ['Dupont', 'Martin', 'Bernard', 'Thomas', 'Robert', 'Richard', 'Petit', 'Durand',
                  'Lefevre', 'Moreau', 'Simon', 'Laurent', 'Lefebvre', 'Michel', 'Garcia', 'David',
                  'Bertrand', 'Roux', 'Vincent', 'Fournier', 'Morel', 'Girod', 'Andre', 'Leroy',
                  'Merle', 'Faure', 'Renault', 'Gérard', 'Noel', 'Caron']
    
    passengers = []
    for i in range(1, 51):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        passenger, created = Passenger.objects.get_or_create(
            email=f'{first_name.lower()}.{last_name.lower()}{i}@example.com',
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'date_of_birth': datetime(random.randint(1950, 2005), random.randint(1, 12), random.randint(1, 28)).date(),
                'phone': f'+33{random.randint(100000000, 999999999)}',
                'passport_number': f'PA{random.randint(100000, 999999)}',
            }
        )
        passengers.append(passenger)
    
    print(f"✓ {len(passengers)} passengers created")
    return passengers

def create_bookings(flights, passengers, users):
    """Create 50 bookings"""
    print("\n🎫 Creating 50 bookings...")
    
    bookings = []
    statuses = ['PENDING', 'CONFIRMED', 'CANCELLED', 'CHECKED_IN']
    
    for i in range(1, 51):
        booking_reference = f'BK{random.randint(10000000, 99999999)}'
        
        flight = random.choice(flights)
        passenger = random.choice(passengers)
        user = random.choice(users) if random.random() > 0.3 else None  # 70% have a user
        
        booking, created = Booking.objects.get_or_create(
            booking_reference=booking_reference,
            defaults={
                'booking_date': datetime.now() - timedelta(days=random.randint(1, 60)),
                'flight': flight,
                'passenger': passenger,
                'user': user,
                'number_of_passengers': random.randint(1, 6),
                'total_price': Decimal(str(round(random.uniform(100, 2000), 2))),
                'status': random.choice(statuses),
                'seat_number': f'{random.randint(1, 40)}{random.choice(["A", "B", "C", "D", "E", "F"])}' if random.random() > 0.2 else None,
            }
        )
        bookings.append(booking)
    
    print(f"✓ {len(bookings)} bookings created")
    return bookings

def create_baggage(bookings):
    """Create 50 baggage records (one per booking)"""
    print("\n🧳 Creating 50 baggage records...")
    
    baggages = []
    statuses = ['REGISTERED', 'CHECKED_IN', 'LOADED', 'IN_TRANSIT', 'DELIVERED', 'LOST']
    
    for i, booking in enumerate(bookings[:50]):
        baggage, created = Baggage.objects.get_or_create(
            booking=booking,
            defaults={
                'weight_kg': Decimal(str(round(random.uniform(5, 32), 2))),
                'status': random.choice(statuses),
            }
        )
        baggages.append(baggage)
    
    print(f"✓ {len(baggages)} baggage records created")
    return baggages

def print_summary():
    """Print summary of created data"""
    print("\n" + "="*50)
    print("📊 DATA SUMMARY")
    print("="*50)
    print(f"Users:       {User.objects.filter(username__startswith='user').count()}")
    print(f"Airports:    {Airport.objects.count()}")
    print(f"Flights:     {Flight.objects.count()}")
    print(f"Passengers:  {Passenger.objects.count()}")
    print(f"Bookings:    {Booking.objects.count()}")
    print(f"Baggage:     {Baggage.objects.count()}")
    print("="*50)

def main():
    """Main function"""
    print("\n🚀 Starting data generation...")
    print("="*50)
    
    try:
        clear_data()
        users = create_users()
        airports = create_airports()
        flights = create_flights(airports)
        passengers = create_passengers()
        bookings = create_bookings(flights, passengers, users)
        create_baggage(bookings)
        print_summary()
        print("\n✅ Data generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
