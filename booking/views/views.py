from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.db.models import Q
from .models import TherapyService, Therapist, TimeSlot, Booking, Review
from .forms import BookingForm, ReviewForm, UserRegistrationForm

def home(request):
    """Home page view with featured services and therapists"""
    services = TherapyService.objects.filter(is_active=True)[:3]
    therapists = Therapist.objects.all()[:3]
    context = {
        'services': services,
        'therapists': therapists,
    }
    return render(request, 'booking/home.html', context)

def services(request):
    """View all therapy services"""
    services = TherapyService.objects.filter(is_active=True)
    context = {
        'services': services,
    }
    return render(request, 'booking/services.html', context)

def service_detail(request, service_id):
    """View details of a specific service"""
    service = get_object_or_404(TherapyService, id=service_id, is_active=True)
    therapists = service.therapists.all()
    context = {
        'service': service,
        'therapists': therapists,
    }
    return render(request, 'booking/service_detail.html', context)

def therapists(request):
    """View all therapists"""
    therapists = Therapist.objects.all()
    context = {
        'therapists': therapists,
    }
    return render(request, 'booking/therapists.html', context)

def therapist_detail(request, therapist_id):
    """View details of a specific therapist"""
    therapist = get_object_or_404(Therapist, id=therapist_id)
    services = therapist.services.filter(is_active=True)
    reviews = Review.objects.filter(booking__therapist=therapist)
    context = {
        'therapist': therapist,
        'services': services,
        'reviews': reviews,
    }
    return render(request, 'booking/therapist_detail.html', context)

@login_required
def booking(request):
    """Book a therapy session"""
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            
            # Get the selected time slot
            time_slot_id = request.POST.get('selected_time')
            if not time_slot_id:
                messages.error(request, 'Please select a time slot')
                return redirect('booking:booking')
            
            time_slot = get_object_or_404(TimeSlot, id=time_slot_id, is_available=True)
            booking.time_slot = time_slot
            booking.therapist = time_slot.therapist
            booking.save()
            
            messages.success(request, 'Your booking has been submitted successfully!')
            return redirect('booking:my_bookings')
    else:
        form = BookingForm(user=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'booking/booking_form.html', context)

@login_required
def get_available_time_slots(request):
    """AJAX view to get available time slots for a date and service"""
    date_str = request.GET.get('date')
    service_id = request.GET.get('service')
    
    if not date_str or not service_id:
        return JsonResponse({'error': 'Missing date or service'}, status=400)
    
    try:
        service = TherapyService.objects.get(id=service_id)
        # Find therapists who offer this service
        therapists = service.therapists.all()
        # Find available time slots for these therapists on the given date
        time_slots = TimeSlot.objects.filter(
            therapist__in=therapists,
            date=date_str,
            is_available=True
        ).order_by('start_time')
        
        slots_data = []
        for slot in time_slots:
            slots_data.append({
                'id': slot.id,
                'therapist_name': str(slot.therapist),
                'start_time': slot.start_time.strftime('%H:%M'),
                'end_time': slot.end_time.strftime('%H:%M'),
            })
        
        return JsonResponse({'time_slots': slots_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def my_bookings(request):
    """View user's bookings"""
    bookings = Booking.objects.filter(client=request.user).order_by('-time_slot__date', '-time_slot__start_time')
    context = {
        'bookings': bookings,
    }
    return render(request, 'booking/my_bookings.html', context)

@login_required
def booking_detail(request, booking_id):
    """View details of a specific booking"""
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    
    # Check if user can leave a review (booking is completed and no review exists)
    can_review = booking.status == 'completed' and not hasattr(booking, 'review')
    review_form = None
    
    if can_review and request.method == 'POST':
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.booking = booking
            review.save()
            messages.success(request, 'Thank you for your review!')
            return redirect('booking:booking_detail', booking_id=booking.id)
    elif can_review:
        review_form = ReviewForm()
    
    context = {
        'booking': booking,
        'can_review': can_review,
        'review_form': review_form,
    }
    return render(request, 'booking/booking_detail.html', context)

@login_required
@require_POST
def cancel_booking(request, booking_id):
    """Cancel a booking"""
    booking = get_object_or_404(Booking, id=booking_id, client=request.user)
    
    # Only allow cancellation if booking is pending or confirmed
    if booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        
        # Make the time slot available again
        time_slot = booking.time_slot
        time_slot.is_available = True
        time_slot.save()
        
        messages.success(request, 'Your booking has been cancelled successfully.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('booking:my_bookings')

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'booking/register.html', context)
