# Quick Reference Guide - Luggage Settings

## 🚀 Quick Start

### For Users
1. Go to booking page
2. Fill passenger info
3. Enter baggage weight and quantity
4. See real-time price calculation
5. Complete booking with total including baggage fees

### For Admins
1. Access Django admin (`/admin/`)
2. Go to "Paramètres de bagages"
3. Edit the policy settings
4. Save changes (applies immediately)

---

## 📊 Default Settings

```
Free Baggage Allowance: 20 kg per passenger
Max Weight per Item: 32 kg
Max Total Weight: 32 kg
Excess Baggage Price: 5 € per kg
```

---

## 💰 Pricing Example

| Scenario | Calculation | Total |
|----------|-------------|-------|
| 15 kg baggage | Flight (150€) + 0€ | 150€ |
| 20 kg baggage | Flight (150€) + 0€ | 150€ |
| 25 kg baggage | Flight (150€) + (5kg × 5€) | 175€ |
| 30 kg baggage | Flight (150€) + (10kg × 5€) | 200€ |

---

## 🗂️ File Locations

### Models
- `ynovair/flights/models.py` - LuggageSettings & Baggage

### Views
- `ynovair/flights/views.py` - booking_create & booking_detail

### Templates
- `ynovair/templates/flights/booking_create.html`
- `ynovair/templates/flights/booking_detail.html`

### Admin
- `ynovair/flights/admin.py` - LuggageSettingsAdmin & BaggageAdmin

### Migrations
- `ynovair/flights/migrations/0005_luggagesettings.py`
- `ynovair/flights/migrations/0006_baggage_extended.py`

---

## 🔧 Common Tasks

### Change Luggage Allowance
1. Login to admin
2. Luggage Settings → Edit
3. Change "Franchise de bagages (kg)"
4. Save

### Change Excess Baggage Price
1. Login to admin
2. Luggage Settings → Edit
3. Change "Prix par kg supplémentaire (€)"
4. Save

### View Booking with Baggage
1. Go to Booking Detail
2. Scroll to "Informations sur les bagages"
3. See all baggage items with charges

### View Baggage Admin
1. Login to admin
2. Baggage menu
3. Filter by booking or date
4. Search by booking reference

---

## 📝 Database Schema

### LuggageSettings Table
```
id                    INTEGER PRIMARY KEY
free_baggage_allowance    DECIMAL(5,2)
max_baggage_per_item      DECIMAL(5,2)
max_total_weight          DECIMAL(5,2)
price_per_extra_kg        DECIMAL(8,2)
is_active                 BOOLEAN
```

### Baggage Table (Extended)
```
id                    INTEGER PRIMARY KEY
booking_id            INTEGER (Foreign Key)
weight_kg             DECIMAL(5,2)
quantity              INTEGER
description           VARCHAR(100)
status                VARCHAR(20)
is_extra              BOOLEAN
```

---

## 🧮 Calculation Formulas

### Excess Weight
```
excess_weight = max(baggage_weight - free_allowance, 0)
```

### Excess Charge
```
excess_charge = excess_weight × price_per_extra_kg
```

### Booking Total
```
total_price = flight_price + excess_charge
```

---

## 🐛 Troubleshooting

### Problem: Luggage section not showing
**Solution**: Check that `LuggageSettings.is_active = True` in database

### Problem: Charges not calculating
**Solution**: 
1. Refresh browser page
2. Check browser console for JavaScript errors
3. Verify `price_per_extra_kg` is not zero

### Problem: Migration error
**Solution**: 
1. Rollback: `python manage.py migrate flights 0004`
2. Check database consistency
3. Re-apply: `python manage.py migrate`

### Problem: Admin not showing new fields
**Solution**: Clear browser cache and reload

---

## 📞 Support Features

### For Customers
- Real-time price preview
- Clear baggage policy display
- Per-item baggage tracking
- Detailed booking confirmation

### For Admins
- Easy policy configuration
- Baggage history and filtering
- Charge calculation verification
- Admin-friendly UI

---

## ✅ Tested & Verified

- ✓ Model creation and relationships
- ✓ Excess weight calculations
- ✓ Charge calculations
- ✓ Real-time JavaScript updates
- ✓ Admin interface functionality
- ✓ Database migrations
- ✓ Template rendering
- ✓ Backward compatibility

---

## 🎯 Key Features

1. **Automatic Calculations** - System calculates excess charges automatically
2. **Real-Time Updates** - Users see price changes as they enter baggage info
3. **Flexible Configuration** - Admins can change policy without code changes
4. **Clear Visualization** - Color-coded baggage display (green/red)
5. **Comprehensive Tracking** - All baggage logged with details
6. **French Support** - Full French language interface

---

**Last Updated**: November 24, 2025
**Version**: 1.0 - Production Ready ✓
