from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TherapyService(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    duration = models.IntegerField(help_text="Duration in minutes")
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class Therapist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    specialization = models.CharField(max_length=100)
    experience_years = models.IntegerField()
    profile_image = models.ImageField(upload_to='therapists/', null=True, blank=True)
    services = models.ManyToManyField(TherapyService, related_name='therapists')
    
    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

class TimeSlot(models.Model):
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='time_slots')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['date', 'start_time']
        unique_together = ['therapist', 'date', 'start_time']
    
    def __str__(self):
        return f"{self.therapist} - {self.date} {self.start_time} to {self.end_time}"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='bookings')
    service = models.ForeignKey(TherapyService, on_delete=models.CASCADE)
    time_slot = models.OneToOneField(TimeSlot, on_delete=models.CASCADE, related_name='booking')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # New field to track if this booking was made using a subscription
    subscription = models.ForeignKey('Subscription', on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    
    class Meta:
        ordering = ['-time_slot__date', '-time_slot__start_time']
    
    def __str__(self):
        return f"{self.client.username} - {self.service.name} with {self.therapist} on {self.time_slot.date}"
    
    def save(self, *args, **kwargs):
        # Mark the time slot as unavailable when booking is created
        if self.status != 'cancelled':
            self.time_slot.is_available = False
            self.time_slot.save()
        super().save(*args, **kwargs)

class Review(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Review by {self.booking.client.username} for {self.booking.service.name}"