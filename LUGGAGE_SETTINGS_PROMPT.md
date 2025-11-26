# Luggage Settings Functionality Prompt for Claude Haiku 4.5

## Context
You are working on a Django airline booking application called "YnovAir" for a school project. The project is simple and functional with the following key components:

### Current Structure:
- **Models**: Airport, Flight, Passenger, Booking, Baggage
- **Views**: Home, search_flights, flight_detail, booking_create, booking_detail, my_bookings
- **Auth**: Custom register, login, logout, profile views
- **Database**: SQLite with existing migrations up to migration 0004
- **UI**: Bootstrap-based templates with French text
- **Language/TZ**: French (fr-fr), Paris timezone

### Current Baggage Model:
```python
class Baggage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2)
    status = models.CharField(max_length=20)
```

---

## Task: Add Luggage Settings Functionality

Implement a simple but complete luggage management system for the airline project. The feature should allow users to configure luggage allowances during the booking process and manage them in their booking details.

### Requirements:

#### 1. **Database Models** (with migration)
- Create a new `LuggageSettings` model to store luggage policies with:
  - `free_baggage_allowance` (kg) - default allowance per passenger
  - `max_baggage_per_item` (kg) - maximum weight per piece
  - `max_total_weight` (kg) - maximum total weight per passenger
  - `price_per_extra_kg` (decimal) - charge for excess baggage
  - `is_active` (boolean)
  
- Extend the existing `Baggage` model to include:
  - `quantity` (number of pieces)
  - `description` (e.g., "Cabin luggage", "Checked baggage")
  - `is_extra` (boolean) - indicates if charged extra

#### 2. **Views** (simple and functional)
- Create `luggage_settings` admin view - display current luggage policy
- Modify `booking_create` view to:
  - Display luggage information before confirmation
  - Allow users to specify their baggage (number of pieces and weight)
  - Calculate excess baggage charges automatically
  - Update booking total_price accordingly
  
- Modify `booking_detail` view to display luggage information

#### 3. **Templates**
- Update `booking_create.html` to include a luggage section showing:
  - Current luggage allowance per passenger
  - Form to specify baggage (pieces and weight)
  - Real-time calculation of excess baggage charges
  
- Update `booking_detail.html` to display:
  - Luggage summary (number of pieces, total weight)
  - Excess baggage charges if applicable
  - Baggage descriptions

#### 4. **Admin Panel**
- Register `LuggageSettings` model with admin
- Allow easy editing of luggage policies
- Display luggage info in Baggage admin

#### 5. **Migrations**
- Create initial migration adding `LuggageSettings` model
- Create migration extending `Baggage` model with new fields

### Implementation Notes:
- Keep the code simple and maintainable for a school project
- Use existing French labels and translations
- Add simple form validation (weight, quantity)
- Use DecimalField for monetary values and weights
- Add helpful comments in code
- Follow Django conventions used in the existing code
- Ensure backward compatibility with existing bookings

### Expected Outcome:
A user can:
1. See luggage allowance during booking
2. Specify their baggage (pieces and weight)
3. See automatic calculation of excess charges
4. Complete booking with luggage info
5. View their luggage details in booking confirmation

---

## Task Execution Steps:
1. Create new `LuggageSettings` model migration (0005_luggagesettings.py)
2. Extend `Baggage` model and create migration (0006_baggage_extended.py)
3. Update `models.py` with new fields
4. Update `admin.py` to register new model
5. Create luggage configuration view (optional simple view)
6. Modify `booking_create` view to handle luggage
7. Modify `booking_detail` view to display luggage
8. Update `booking_create.html` template
9. Update `booking_detail.html` template
10. Test all migrations and functionality

## Notes:
- Make it work with the existing booking flow
- Keep the UI consistent with current design
- Provide meaningful error messages in French where applicable
- The system should be production-ready but simple for a school project
