# Script to initialize default luggage settings
# Run this with: python manage.py shell < init_luggage_settings.py

from flights.models import LuggageSettings

# Check if luggage settings already exist
if not LuggageSettings.objects.exists():
    LuggageSettings.objects.create(
        free_baggage_allowance=20,
        max_baggage_per_item=32,
        max_total_weight=32,
        price_per_extra_kg=5,
        is_active=True
    )
    print("✓ Default luggage settings created successfully!")
else:
    print("✓ Luggage settings already exist")

# Display current settings
settings = LuggageSettings.objects.filter(is_active=True).first()
if settings:
    print("\nCurrent Luggage Settings:")
    print(f"  - Free baggage allowance: {settings.free_baggage_allowance} kg")
    print(f"  - Max baggage per item: {settings.max_baggage_per_item} kg")
    print(f"  - Max total weight: {settings.max_total_weight} kg")
    print(f"  - Price per extra kg: {settings.price_per_extra_kg} €")
