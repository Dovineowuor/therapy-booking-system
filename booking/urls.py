from django.urls import path
from . import views
from .views import (
    membership_plans, subscribe, payment, subscription_success,
    my_subscriptions, cancel_subscription
)

app_name = 'booking'

urlpatterns = [
    # Booking related URLs
    path('services/', views.services, name='services'),
    path('services/<int:service_id>/', views.service_detail, name='service_detail'),
    path('therapists/', views.therapists, name='therapists'),
    path('therapists/<int:therapist_id>/', views.therapist_detail, name='therapist_detail'),
    path('booking/', views.booking, name='booking'),
    path('get-time-slots/', views.get_available_time_slots, name='get_time_slots'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('my-bookings/<int:booking_id>/', views.booking_detail, name='booking_detail'),
    path('my-bookings/<int:booking_id>/cancel/', views.cancel_booking, name='cancel_booking'),
    
    # Membership and subscription related URLs
    path('memberships/', membership_plans, name='membership_plans'),
    path('subscribe/', subscribe, name='subscribe'),
    path('subscribe/<int:plan_id>/', subscribe, name='subscribe_to_plan'),
    path('payment/<uuid:subscription_id>/', payment, name='payment'),
    path('subscription/success/<uuid:subscription_id>/', subscription_success, name='subscription_success'),
    path('my-subscriptions/', my_subscriptions, name='my_subscriptions'),
    path('subscription/<uuid:subscription_id>/cancel/', cancel_subscription, name='cancel_subscription'),
]