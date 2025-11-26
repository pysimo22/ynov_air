#!/usr/bin/env python
"""
Delete baggage records from the database
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ynov_air.settings')
django.setup()

from flights.models import Baggage

# Option 1: Delete ALL baggage
print("🗑️  Deleting all baggage records...")
count, _ = Baggage.objects.all().delete()
print(f"✅ Deleted {count} baggage records")

# Option 2: Delete baggage by specific booking (uncomment to use)
# from flights.models import Booking
# booking_id = 1
# booking = Booking.objects.get(id=booking_id)
# count, _ = Baggage.objects.filter(booking=booking).delete()
# print(f"✅ Deleted {count} baggage records for booking {booking_id}")

# Option 3: Delete baggage by status (uncomment to use)
# status = 'LOST'
# count, _ = Baggage.objects.filter(status=status).delete()
# print(f"✅ Deleted {count} baggage records with status {status}")
