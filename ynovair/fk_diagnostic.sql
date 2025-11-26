-- ============================================================================
-- FOREIGN KEY DIAGNOSTIC QUERIES FOR YNOVAIR DATABASE
-- ============================================================================

-- ============================================================================
-- 1. LIST ALL FOREIGN KEYS IN THE DATABASE
-- ============================================================================
SELECT 
    table_name,
    column_name,
    constraint_name,
    referenced_table_name,
    referenced_column_name
FROM information_schema.key_column_usage
WHERE table_schema = DATABASE() AND referenced_table_name IS NOT NULL
ORDER BY table_name, column_name;

-- SQLite Alternative (if using SQLite):
PRAGMA foreign_key_list(flights_booking);
PRAGMA foreign_key_list(flights_baggage);
PRAGMA foreign_key_list(flights_flight);


-- ============================================================================
-- 2. CHECK FLIGHTS_BOOKING TABLE FOR INVALID FOREIGN KEYS
-- ============================================================================

-- Bookings with invalid flight_id references
SELECT 
    b.id,
    b.booking_reference,
    b.flight_id,
    CASE WHEN f.id IS NULL THEN 'INVALID - Flight does not exist' ELSE 'OK' END as flight_status
FROM flights_booking b
LEFT JOIN flights_flight f ON b.flight_id = f.id
WHERE f.id IS NULL;

-- Bookings with invalid passenger_id references
SELECT 
    b.id,
    b.booking_reference,
    b.passenger_id,
    CASE WHEN p.id IS NULL THEN 'INVALID - Passenger does not exist' ELSE 'OK' END as passenger_status
FROM flights_booking b
LEFT JOIN flights_passenger p ON b.passenger_id = p.id
WHERE p.id IS NULL;

-- Bookings with invalid user_id references (user_id can be NULL, so check only non-NULL)
SELECT 
    b.id,
    b.booking_reference,
    b.user_id,
    CASE WHEN u.id IS NULL THEN 'INVALID - User does not exist' ELSE 'OK' END as user_status
FROM flights_booking b
LEFT JOIN auth_user u ON b.user_id = u.id
WHERE b.user_id IS NOT NULL AND u.id IS NULL;


-- ============================================================================
-- 3. CHECK FLIGHTS_BAGGAGE TABLE FOR INVALID FOREIGN KEYS
-- ============================================================================

-- Baggage with invalid booking_id references
SELECT 
    bg.id,
    bg.booking_id,
    CASE WHEN b.id IS NULL THEN 'INVALID - Booking does not exist' ELSE 'OK' END as booking_status
FROM flights_baggage bg
LEFT JOIN flights_booking b ON bg.booking_id = b.id
WHERE b.id IS NULL;


-- ============================================================================
-- 4. CHECK FLIGHTS_FLIGHT TABLE FOR INVALID FOREIGN KEYS
-- ============================================================================

-- Flights with invalid airport references (departure_airport_id)
SELECT 
    f.id,
    f.flight_number,
    f.departure_airport_id,
    CASE WHEN a.id IS NULL THEN 'INVALID - Airport does not exist' ELSE 'OK' END as departure_airport_status
FROM flights_flight f
LEFT JOIN flights_airport a ON f.departure_airport_id = a.id
WHERE a.id IS NULL;

-- Flights with invalid airport references (arrival_airport_id)
SELECT 
    f.id,
    f.flight_number,
    f.arrival_airport_id,
    CASE WHEN a.id IS NULL THEN 'INVALID - Airport does not exist' ELSE 'OK' END as arrival_airport_status
FROM flights_flight f
LEFT JOIN flights_airport a ON f.arrival_airport_id = a.id
WHERE a.id IS NULL;


-- ============================================================================
-- 5. COMPREHENSIVE INTEGRITY CHECK - ALL TABLES
-- ============================================================================

-- Summary of all constraint violations
SELECT 
    'flights_booking → flight_id' as constraint_name,
    COUNT(*) as violation_count
FROM flights_booking b
LEFT JOIN flights_flight f ON b.flight_id = f.id
WHERE f.id IS NULL
UNION ALL
SELECT 
    'flights_booking → passenger_id',
    COUNT(*)
FROM flights_booking b
LEFT JOIN flights_passenger p ON b.passenger_id = p.id
WHERE p.id IS NULL
UNION ALL
SELECT 
    'flights_booking → user_id (non-NULL only)',
    COUNT(*)
FROM flights_booking b
LEFT JOIN auth_user u ON b.user_id = u.id
WHERE b.user_id IS NOT NULL AND u.id IS NULL
UNION ALL
SELECT 
    'flights_baggage → booking_id',
    COUNT(*)
FROM flights_baggage bg
LEFT JOIN flights_booking b ON bg.booking_id = b.id
WHERE b.id IS NULL
UNION ALL
SELECT 
    'flights_flight → departure_airport_id',
    COUNT(*)
FROM flights_flight f
LEFT JOIN flights_airport a ON f.departure_airport_id = a.id
WHERE a.id IS NULL
UNION ALL
SELECT 
    'flights_flight → arrival_airport_id',
    COUNT(*)
FROM flights_flight f
LEFT JOIN flights_airport a ON f.arrival_airport_id = a.id
WHERE a.id IS NULL;


-- ============================================================================
-- 6. DATA EXISTENCE VERIFICATION
-- ============================================================================

-- Count records in each table
SELECT 
    'flights_airport' as table_name,
    COUNT(*) as record_count
FROM flights_airport
UNION ALL
SELECT 'flights_flight', COUNT(*) FROM flights_flight
UNION ALL
SELECT 'flights_passenger', COUNT(*) FROM flights_passenger
UNION ALL
SELECT 'flights_booking', COUNT(*) FROM flights_booking
UNION ALL
SELECT 'flights_baggage', COUNT(*) FROM flights_baggage
UNION ALL
SELECT 'auth_user', COUNT(*) FROM auth_user;


-- ============================================================================
-- 7. FIXES FOR COMMON ISSUES
-- ============================================================================

-- FIX 1: Delete bookings with invalid flight references
-- DELETE FROM flights_booking 
-- WHERE flight_id NOT IN (SELECT id FROM flights_flight);

-- FIX 2: Delete bookings with invalid passenger references
-- DELETE FROM flights_booking 
-- WHERE passenger_id NOT IN (SELECT id FROM flights_passenger);

-- FIX 3: Delete bookings with invalid user references (if user_id is NOT NULL)
-- DELETE FROM flights_booking 
-- WHERE user_id IS NOT NULL AND user_id NOT IN (SELECT id FROM auth_user);

-- FIX 4: Delete baggage with invalid booking references
-- DELETE FROM flights_baggage 
-- WHERE booking_id NOT IN (SELECT id FROM flights_booking);

-- FIX 5: Delete flights with invalid airport references
-- DELETE FROM flights_flight 
-- WHERE departure_airport_id NOT IN (SELECT id FROM flights_airport)
--    OR arrival_airport_id NOT IN (SELECT id FROM flights_airport);

-- FIX 6: Set user_id to NULL for bookings where user doesn't exist
-- UPDATE flights_booking 
-- SET user_id = NULL 
-- WHERE user_id IS NOT NULL AND user_id NOT IN (SELECT id FROM auth_user);
