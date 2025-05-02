from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

from booking.models.booking import TherapyService as Service, Therapist, TimeSlot, Booking
from booking.models.membership import Subscription
from booking.forms.booking_forms import BookingForm
from booking.forms.auth_forms import CustomUserCreationForm

@csrf_exempt
def custom_login(request):
    """Custom login view with CSRF exemption for development"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def home(request):
    """Home page view"""
    services = Service.objects.all()[:3]  # Get 3 featured services
    therapists = Therapist.objects.all()[:3]  # Get 3 featured therapists
    
    context = {
        'services': services,
        'therapists': therapists,
        'is_home': True
    }
    return render(request, 'booking/home.html', context)

def services(request):
    """View to display all services"""
    services = Service.objects.all()
    context = {
        'services': services
    }
    return render(request, 'booking/services.html', context)

def service_detail(request, service_id):
    """View to display details of a specific service"""
    service = get_object_or_404(Service, id=service_id)
    therapists = Therapist.objects.filter(services=service)
    context = {
        'service': service,
        'therapists': therapists
    }
    return render(request, 'booking/service_detail.html', context)

def therapists(request):
    """View to display all therapists"""
    therapists = Therapist.objects.all()
    context = {
        'therapists': therapists
    }
    return render(request, 'booking/therapists.html', context)

def therapist_detail(request, therapist_id):
    """View to display details of a specific therapist"""
    therapist = get_object_or_404(Therapist, id=therapist_id)
    services = therapist.services.all()
    context = {
        'therapist': therapist,
        'services': services
    }
    return render(request, 'booking/therapist_detail.html', context)

@login_required
def booking(request):
    """View to create a new booking"""
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            print("Form is valid")
            print("Form data:", form.cleaned_data)
            print("Time slot ID from POST:", request.POST.get('time_slot'))
            
            # Get the selected time slot
            time_slot_id = request.POST.get('time_slot')
            if not time_slot_id:
                messages.error(request, 'Please select a time slot')
                return redirect('booking:booking')
            
            try:
                time_slot = TimeSlot.objects.get(id=time_slot_id)
                print("Found time slot:", time_slot)
            except TimeSlot.DoesNotExist:
                messages.error(request, 'Invalid time slot selected')
                return redirect('booking:booking')
            
            # Create the booking
            booking = form.save(commit=False)
            print("Booking object created:", booking)
            booking.time_slot = time_slot
            print("Time slot assigned to booking")
            booking.save()
            print("Booking saved to database")
            
            # Mark the time slot as unavailable
            time_slot.is_available = False
            time_slot.save()
            print("Time slot marked as unavailable")
            
            messages.success(request, 'Your booking has been confirmed!')
            return redirect('booking:booking_detail', booking_id=booking.id)
        else:
            print("Form is invalid")
            print("Form errors:", form.errors)
            messages.error(request, 'There was an error with your booking. Please check the form and try again.')
    else:
        # Pre-select service or therapist if provided in query params
        initial_data = {}
        if 'service_id' in request.GET:
            try:
                service = Service.objects.get(id=request.GET['service_id'])
                initial_data['service'] = service
            except Service.DoesNotExist:
                pass
        
        if 'therapist_id' in request.GET:
            try:
                therapist = Therapist.objects.get(id=request.GET['therapist_id'])
                initial_data['therapist'] = therapist
            except Therapist.DoesNotExist:
                pass
        
        form = BookingForm(user=request.user, initial=initial_data)
    
    # Check if user has an active subscription
    active_subscription = None
    if request.user.is_authenticated:
        active_subscription = Subscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now(),
            sessions_remaining__gt=0
        ).first()
    
    context = {
        'form': form,
        'active_subscription': active_subscription
    }
    return render(request, 'booking/booking_form.html', context)

def get_available_time_slots(request):
    """AJAX view to get available time slots for a specific date and therapist"""
    date_str = request.GET.get('date')
    therapist_id = request.GET.get('therapist_id')
    
    if not date_str or not therapist_id:
        return JsonResponse({'error': 'Date and therapist are required'}, status=400)
    
    try:
        date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        therapist = Therapist.objects.get(id=therapist_id)
    except (ValueError, Therapist.DoesNotExist):
        return JsonResponse({'error': 'Invalid date or therapist'}, status=400)
    
    # Get all available time slots for the therapist on the selected date
    time_slots = TimeSlot.objects.filter(
        therapist=therapist,
        date=date,
        is_available=True
    )
    
    # Filter out the time slots that are already booked
    available_time_slots = time_slots.filter(is_available=True)
    
    # Format the time slots for the response
    formatted_time_slots = []
    for slot in available_time_slots:
        formatted_time_slots.append({
            'start_time': slot.start_time.strftime('%H:%M'),
            'end_time': slot.end_time.strftime('%H:%M'),
            'display': f"{slot.start_time.strftime('%I:%M %p')} - {slot.end_time.strftime('%I:%M %p')}"
        })
    
    return JsonResponse({'time_slots': formatted_time_slots})

@login_required
def my_bookings(request):
    """View to display user's bookings"""
    bookings = Booking.objects.filter(client=request.user).order_by('-time_slot__date', '-time_slot__start_time')
    
    # Separate bookings into upcoming and past
    today = timezone.now().date()
    upcoming_bookings = bookings.filter(time_slot__date__gte=today)
    past_bookings = bookings.filter(time_slot__date__lt=today)
    
    context = {
        'upcoming_bookings': upcoming_bookings,
        'past_bookings': past_bookings
    }
    return render(request, 'booking/my_bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    """View to display details of a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    context = {
        'booking': booking
    }
    return render(request, 'booking/booking_detail.html', context)

@login_required
@require_POST
def cancel_booking(request, booking_id):
    """View to cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    
    # Check if booking can be cancelled (not in the past)
    if booking.time_slot.date < timezone.now().date():
        messages.error(request, 'You cannot cancel a booking that has already passed.')
        return redirect('booking:booking_detail', booking_id=booking.id)
    
    # If booking was made with a subscription, refund the session
    if booking.subscription:
        subscription = booking.subscription
        subscription.sessions_remaining += 1
        subscription.save()
    
    booking.status = 'cancelled'
    booking.save()
    
    messages.success(request, 'Your booking has been cancelled.')
    return redirect('booking:my_bookings')

@csrf_exempt
def register(request):
    """View for user registration with CSRF exemption for development"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Welcome, {user.first_name}! Your account has been created successfully.')
            return redirect('home')
        else:
            # Print form errors for debugging
            print(f"Form errors: {form.errors}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})