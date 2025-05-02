from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponseRedirect

from booking.models import MembershipPlan, Subscription, SubscriptionPayment
from booking.forms import SubscriptionForm, PaymentForm

@login_required
def membership_plans(request):
    """View to display available membership plans"""
    plans = MembershipPlan.objects.filter(is_active=True)
    
    # Check if user already has an active subscription
    active_subscription = None
    try:
        active_subscription = Subscription.objects.filter(
            user=request.user,
            status='active',
            end_date__gt=timezone.now()
        ).first()
    except:
        pass
    
    context = {
        'plans': plans,
        'active_subscription': active_subscription
    }
    return render(request, 'booking/membership/plans.html', context)

@login_required
def subscribe(request, plan_id=None):
    """View to subscribe to a membership plan"""
    # If plan_id is provided, pre-select that plan
    initial_data = {}
    if plan_id:
        plan = get_object_or_404(MembershipPlan, id=plan_id, is_active=True)
        initial_data = {'plan': plan}
    
    if request.method == 'POST':
        form = SubscriptionForm(request.POST, user=request.user, initial=initial_data)
        if form.is_valid():
            subscription = form.save()
            
            # Redirect to payment page
            return redirect('booking:payment', subscription_id=subscription.id)
    else:
        form = SubscriptionForm(user=request.user, initial=initial_data)
    
    context = {
        'form': form,
    }
    return render(request, 'booking/membership/subscribe.html', context)

@login_required
def payment(request, subscription_id):
    """View to process payment for a subscription"""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    
    # Check if subscription is already active
    if subscription.status == 'active':
        messages.info(request, 'This subscription is already active.')
        return redirect('booking:my_subscriptions')
    
    if request.method == 'POST':
        form = PaymentForm(request.POST, subscription=subscription)
        if form.is_valid():
            payment = form.save()
            
            messages.success(request, 'Payment successful! Your subscription is now active.')
            return redirect('booking:subscription_success', subscription_id=subscription.id)
    else:
        form = PaymentForm(subscription=subscription)
    
    context = {
        'form': form,
        'subscription': subscription,
        'amount': subscription.plan.price,
        'plan_name': subscription.plan.name
    }
    return render(request, 'booking/membership/payment.html', context)

@login_required
def subscription_success(request, subscription_id):
    """View to display subscription success page"""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    
    context = {
        'subscription': subscription
    }
    return render(request, 'booking/membership/success.html', context)

@login_required
def my_subscriptions(request):
    """View to display user's subscriptions"""
    subscriptions = Subscription.objects.filter(user=request.user).order_by('-created_at')
    
    active_subscription = subscriptions.filter(
        status='active',
        end_date__gt=timezone.now()
    ).first()
    
    context = {
        'subscriptions': subscriptions,
        'active_subscription': active_subscription
    }
    return render(request, 'booking/membership/my_subscriptions.html', context)

@login_required
def cancel_subscription(request, subscription_id):
    """View to cancel a subscription"""
    subscription = get_object_or_404(Subscription, id=subscription_id, user=request.user)
    
    if request.method == 'POST':
        subscription.status = 'cancelled'
        subscription.auto_renew = False
        subscription.save()
        
        messages.success(request, 'Your subscription has been cancelled.')
        return redirect('booking:my_subscriptions')
    
    context = {
        'subscription': subscription
    }
    return render(request, 'booking/membership/cancel.html', context)