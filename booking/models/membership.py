from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import datetime

class MembershipPlan(models.Model):
    """Model for different membership plans"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.PositiveIntegerField(help_text="Duration in days")
    sessions_included = models.PositiveIntegerField(default=0, help_text="Number of therapy sessions included")
    discount_percent = models.PositiveIntegerField(default=0, help_text="Discount percentage on additional sessions")
    is_active = models.BooleanField(default=True)
    features = models.JSONField(default=list, help_text="List of features included in this plan")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    """Model for user subscriptions to membership plans"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
        ('pending', 'Pending'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name='subscriptions')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    sessions_remaining = models.PositiveIntegerField(default=0)
    auto_renew = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s {self.plan.name} subscription"
    
    def save(self, *args, **kwargs):
        # If this is a new subscription, set the end date and sessions remaining
        if not self.pk:
            self.end_date = self.start_date + timezone.timedelta(days=self.plan.duration_days)
            self.sessions_remaining = self.plan.sessions_included
        super().save(*args, **kwargs)
    
    def is_active(self):
        now = timezone.now()
        if isinstance(self.end_date, datetime.date):
            now = now.date()
        return self.status == 'active' and self.end_date > now
    
    def days_remaining(self):
        if not self.is_active():
            return 0
        delta = self.end_date - timezone.now()
        return max(0, delta.days)

class SubscriptionPayment(models.Model):
    """Model for tracking subscription payments"""
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(default=timezone.now)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Payment {self.id} for {self.subscription}"