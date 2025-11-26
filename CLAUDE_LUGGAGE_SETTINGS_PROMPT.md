# Claude 4.5 Haiku - Luggage Settings Implementation Prompt

## Project Context
**Project**: YnovAir - Django Airline Booking System (School Project)
**Language**: French (UI/translations)
**Framework**: Django 5.2.8 with SQLite database
**Users**: Authenticated users only
**Architecture**: Standard Django MTV (Model-Template-View)

---

## Current Implementation Status

### ✅ What Already Exists:
1. **Baggage Model** - Currently exists with:
   - `booking` (ForeignKey to Booking)
   - `quantity`, `weight_kg`, `description`, `is_extra`, `status`
   - Methods: `get_excess_weight()`, `calculate_extra_charge()`
   - Hardcoded values: 20kg free allowance, €5/kg extra charge

2. **Booking Form** (`booking_create.html`) - Already has:
   - Baggage input fields (quantity, weight, description)
   - Real-time JavaScript price calculation
   - Display of hardcoded luggage policy (20kg free, €5/kg)

3. **Views** (`flights/views.py`) - Already has:
   - `booking_create()` - Handles baggage creation with transaction.atomic()
   - `booking_detail()` - Shows baggage info and calculates charges
   - `my_bookings()` - Filters by authenticated user

4. **Admin Interface** - Has BaggageAdmin configured

---

## Task: Implement LuggageSettings Configuration Model

### Objective:
Replace hardcoded baggage values with a configurable **LuggageSettings** model that admin users can manage. Keep it simple and functional for a school project.

---

## Detailed Requirements

### 1. Create LuggageSettings Model
**File**: `flights/models.py`

Add a new model with these fields:
- `free_baggage_allowance` (DecimalField, default=20kg)
- `max_baggage_per_item` (DecimalField, default=32kg)
- `max_total_weight` (DecimalField, default=100kg)
- `price_per_extra_kg` (DecimalField, default=5€)
- `is_active` (BooleanField, default=True)

**Constraints**:
- Use `DecimalField(max_digits=5, decimal_places=2)` for weights
- Use `DecimalField(max_digits=8, decimal_places=2)` for prices
- Add `verbose_name` fields in French
- Add Meta class with French verbose_name_plural
- Add `__str__()` method returning "Configuration des bagages"

---

### 2. Update Baggage Model Methods
**File**: `flights/models.py`

Modify `Baggage.get_excess_weight()` and `Baggage.calculate_extra_charge()` to:
- Query the active LuggageSettings instance
- Fall back to defaults if no settings exist
- Handle None values gracefully
- Add null check for `weight_kg`

**Keep the logic simple**:
```
get_excess_weight():
  - If weight_kg is None: return 0
  - Get active LuggageSettings
  - If weight > free_allowance: return excess
  - Else: return 0

calculate_extra_charge():
  - Get excess_weight()
  - Multiply by price_per_extra_kg
  - Return total
```

---

### 3. Create Database Migration
**File**: `flights/migrations/000X_luggagesettings.py`

Generate with `python manage.py makemigrations` but verify it includes:
- CreateModel operation for LuggageSettings
- Proper field definitions with defaults
- Unique constraint (optional, only 1 active settings)

---

### 4. Update Views
**File**: `flights/views.py`

**`booking_create()` view**:
- Import: `from .models import ... LuggageSettings`
- Replace: `luggage_settings = None` with query for active settings
- Update validation to use `luggage_settings.max_baggage_per_item`

**`booking_detail()` view**:
- Update to query active LuggageSettings
- Pass to template context

---

### 5. Register Admin Interface
**File**: `flights/admin.py`

Create `LuggageSettingsAdmin` class with:
- `list_display`: All fields including `is_active`
- `fieldsets`: Organize into sections (Franchise, Pricing, Status)
- `has_delete_permission()`: Return False to prevent deletion
- Add `@admin.register(LuggageSettings)` decorator

**Example fieldsets**:
```
('Franchise de bagages', {'fields': ('free_baggage_allowance', 'max_baggage_per_item', 'max_total_weight')}),
('Tarification', {'fields': ('price_per_extra_kg',)}),
('État', {'fields': ('is_active',)})
```

---

### 6. Update Templates
**File**: `templates/flights/booking_create.html`

Replace hardcoded display:
```html
{% if luggage_settings %}
  <p>Franchise: {{ luggage_settings.free_baggage_allowance }} kg</p>
  <p>Max par bagage: {{ luggage_settings.max_baggage_per_item }} kg</p>
  <p>Tarif extra: {{ luggage_settings.price_per_extra_kg }} €/kg</p>
{% endif %}
```

Update JavaScript to use template variables:
```javascript
const freeAllowance = {{ luggage_settings.free_baggage_allowance|default:20 }};
const pricePerExtraKg = {{ luggage_settings.price_per_extra_kg|default:5 }};
```

**File**: `templates/flights/booking_detail.html`

Update to display:
- `luggage_settings.free_baggage_allowance` in baggage section
- Calculated charges using `baggage.calculate_extra_charge()`

---

## Implementation Steps (in order)

1. **Add LuggageSettings model** to `models.py`
2. **Update Baggage model methods** to query LuggageSettings
3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. **Update views** to use `LuggageSettings.objects.filter(is_active=True).first()`
5. **Register admin** for LuggageSettings
6. **Update templates** to use `luggage_settings` from context
7. **Test workflow**:
   - Create settings in admin
   - Create booking with baggage
   - Verify charges calculate correctly
   - Verify settings show in booking_create and booking_detail

---

## Error Handling & Edge Cases

1. **No active settings exist**: Fall back to hardcoded defaults (20kg, €5/kg)
2. **Multiple settings**: Query only `is_active=True` (assume only 1)
3. **Null weight_kg**: Return 0 for excess weight
4. **Prevent deletion**: Override `has_delete_permission()` to return False

---

## Code Quality Requirements

- Use French comments and docstrings
- Add `verbose_name` to all model fields
- Use `DecimalField` (not Float) for money/weights
- Add proper `Meta` classes
- Use `@login_required` decorators where needed
- Handle transactions with `transaction.atomic()` in views

---

## Database Considerations

- SQLite with timeout configured (already set in settings)
- Single LuggageSettings instance (UNIQUE constraint optional)
- No data loss on Baggage when LuggageSettings queries fail

---

## Testing Checklist

After implementation:
- [ ] Settings appear in Django admin
- [ ] Can create/edit settings in admin
- [ ] Cannot delete settings (permission denied)
- [ ] Booking form shows dynamic luggage settings
- [ ] Baggage charges calculate correctly
- [ ] Booking detail shows applied prices
- [ ] Fallback to defaults if settings missing
- [ ] No template errors or 500 errors

---

## Notes for School Project

- Keep it simple: Don't over-engineer
- Single active setting is sufficient
- French UI/translations already in place
- Focus on core functionality, not edge cases
- SQLite is fine for school project
- No need for complex permissions

---

## Files to Modify

1. `flights/models.py` - Add LuggageSettings, update Baggage methods
2. `flights/views.py` - Update booking_create, booking_detail
3. `flights/admin.py` - Add LuggageSettingsAdmin
4. `templates/flights/booking_create.html` - Update hardcoded values
5. `templates/flights/booking_detail.html` - Update display
6. Run `python manage.py makemigrations` + `python manage.py migrate`

---

## Success Criteria

✅ LuggageSettings model created and migrated
✅ Admin can manage luggage settings
✅ Booking form uses dynamic settings
✅ Baggage charges calculate from settings
✅ Booking detail displays applied prices
✅ All templates render without errors
✅ No hardcoded values remain (except fallback defaults)
