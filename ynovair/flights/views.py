from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from .models import Flight, Airport, Passenger, Booking, Baggage
import random
import string
from django.contrib.auth.decorators import login_required
from decimal import Decimal


def home(request):
    """Page d'accueil avec recherche de vols"""
    airports = Airport.objects.all()
    upcoming_flights = Flight.objects.filter(
        departure_time__gte=timezone.now(),
        status='SCHEDULED'
    ).order_by('departure_time')[:6]

    context = {
        'airports': airports,
        'upcoming_flights': upcoming_flights,
    }
    return render(request, 'flights/home.html', context)


def search_flights(request):
    """Recherche de vols"""
    flights = []

    if request.method == 'GET':
        origin_id = request.GET.get('origin')
        destination_id = request.GET.get('destination')
        date = request.GET.get('date')

        if origin_id and destination_id:
            flights = Flight.objects.filter(
                origin_id=origin_id,
                destination_id=destination_id,
                status='SCHEDULED'
            )

            if date:
                flights = flights.filter(departure_time__date=date)

            flights = flights.order_by('departure_time')

    airports = Airport.objects.all()
    context = {
        'flights': flights,
        'airports': airports,
    }
    return render(request, 'flights/search.html', context)


def flight_detail(request, flight_id):
    """Détails d'un vol"""
    flight = get_object_or_404(Flight, id=flight_id)
    context = {'flight': flight}
    return render(request, 'flights/flight_detail.html', context)

@login_required
def booking_create(request, flight_id):
    """Créer une réservation avec gestion des bagages"""
    flight = get_object_or_404(Flight, id=flight_id)
    luggage_settings = None  # No LuggageSettings model anymore

    if request.method == 'POST':
        try:
            # Récupérer et valider les données du formulaire AVANT la transaction
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            passport_number = request.POST.get('passport_number', '').strip()
            date_of_birth = request.POST.get('date_of_birth', '')
            baggage_weight = request.POST.get('baggage_weight')
            baggage_quantity = request.POST.get('baggage_quantity')
            baggage_description = request.POST.get('baggage_description', '').strip()
            number_of_passengers = int(request.POST.get('number_of_passengers', 1))
            
            # Valider les saisies
            if not all([first_name, last_name, email, phone]):
                messages.error(request, "Tous les champs requis doivent être complétés.")
                return redirect('flight_detail', flight_id=flight.id)
            
            # Traiter et valider les bagages avant la transaction
            processed_baggage = None
            if baggage_weight and baggage_quantity:
                try:
                    baggage_weight_decimal = Decimal(baggage_weight)
                    baggage_quantity_int = int(baggage_quantity)
                    
                    # Hardcoded defaults
                    max_baggage_per_item = Decimal('32')
                    free_baggage_allowance = Decimal('20')
                    
                    if baggage_weight_decimal > max_baggage_per_item:
                        messages.error(
                            request,
                            f"Le poids du bagage dépasse le maximum autorisé de {max_baggage_per_item} kg."
                        )
                        return redirect('flight_detail', flight_id=flight.id)
                    
                    processed_baggage = {
                        'weight': baggage_weight_decimal,
                        'quantity': baggage_quantity_int,
                        'description': baggage_description,
                        'is_extra': baggage_weight_decimal > free_baggage_allowance
                    }
                except (ValueError, TypeError):
                    messages.error(request, "Données de bagage invalides.")
                    return redirect('flight_detail', flight_id=flight.id)
            
            with transaction.atomic():
                # Générer une référence unique
                booking_reference = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

                if flight.available_seats >= number_of_passengers:
                    # Créer le passager
                    passenger = Passenger.objects.create(
                        first_name=first_name,
                        last_name=last_name,
                        email=email,
                        phone=phone,
                        passport_number=passport_number,
                        date_of_birth=date_of_birth if date_of_birth else None
                    )
                    
                    # Calculer le prix total incluant les frais de bagages
                    total_price = Decimal(flight.price) * number_of_passengers
                    
                    if processed_baggage:
                        # Hardcoded defaults
                        free_baggage_allowance = Decimal('20')
                        price_per_extra_kg = Decimal('5')
                        
                        if processed_baggage['weight'] > free_baggage_allowance:
                            excess_weight = processed_baggage['weight'] - free_baggage_allowance
                            excess_charge = excess_weight * price_per_extra_kg
                            total_price += excess_charge
                    
                    # Créer la réservation
                    booking = Booking.objects.create(
                        booking_reference=booking_reference,
                        flight=flight,
                        passenger=passenger,
                        user=request.user,
                        number_of_passengers=number_of_passengers,
                        total_price=total_price,
                        status='CONFIRMED'
                    )
                    
                    # Créer l'enregistrement de bagage si des informations ont été fournies
                    if processed_baggage:
                        Baggage.objects.create(
                            booking=booking,
                            weight_kg=processed_baggage['weight'],
                            status='REGISTERED'
                        )
                    
                    messages.success(request, f'Réservation confirmée ! Référence: {booking_reference}')
                    return redirect('booking_detail', booking_id=booking.id)
                else:
                    messages.error(request, 'Pas assez de sièges disponibles.')
                    return redirect('flight_detail', flight_id=flight.id)

        except Exception as e:
            messages.error(request, f'Erreur lors de la création de la réservation: {str(e)}')
            return redirect('flight_detail', flight_id=flight.id)

    context = {
        'flight': flight,
        'luggage_settings': luggage_settings
    }
    return render(request, 'flights/booking_create.html', context)


def booking_detail(request, booking_id):
    """Détails d'une réservation avec informations sur les bagages"""
    booking = get_object_or_404(Booking, id=booking_id)
    baggages = booking.baggages.all()
    luggage_settings = None  # No LuggageSettings model
    
    # Calculer les statistiques de bagages
    total_baggage_weight = sum(baggage.weight_kg for baggage in baggages) if baggages else Decimal('0')
    total_excess_charge = sum(baggage.calculate_extra_charge() for baggage in baggages) if baggages else Decimal('0')
    
    # Calculer le prix du vol
    flight_total = booking.flight.price * booking.number_of_passengers
    
    context = {
        'booking': booking,
        'baggages': baggages,
        'luggage_settings': luggage_settings,
        'total_baggage_weight': total_baggage_weight,
        'total_excess_charge': total_excess_charge,
        'flight_total': flight_total
    }
    return render(request, 'flights/booking_detail.html', context)


@login_required
def my_bookings(request):
    """Liste des réservations de l'utilisateur connecté"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    context = {'bookings': bookings}
    return render(request, 'flights/my_bookings.html', context)
