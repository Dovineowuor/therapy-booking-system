from django import forms
from django.utils import timezone
from booking.models import Booking, TherapyService as Service, Therapist, TimeSlot
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML

class BookingForm(forms.ModelForm):
    """Form for creating a new booking"""
    
    date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
        help_text="Select a date for your appointment"
    )
    
    time_slot = forms.ChoiceField(
        choices=[],
        widget=forms.Select(attrs={'class': 'form-control', 'required': True}),
        help_text="Select a time slot for your appointment",
        required=True
    )
    
    use_subscription = forms.BooleanField(
        required=False,
        label="Use my subscription",
        help_text="Check this to use your active subscription for this booking",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = Booking
        fields = ['service', 'therapist', 'date', 'time_slot', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Set up crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4">Book Your Therapy Session</h3>'),
            Row(
                Column('service', css_class='form-group col-md-6 mb-0'),
                Column('therapist', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('date', css_class='form-group col-md-6 mb-0'),
                Column(
                    HTML('''
                    <div class="form-group">
                        <label for="time_slots">Time Slot</label>
                        <div id="time_slots" class="time-slots-container">
                            <div class="alert alert-info">
                                Please select a date and therapist to see available time slots
                            </div>
                        </div>
                        <input type="hidden" name="time_slot" id="id_time_slot">
                    </div>
                    '''),
                    css_class='form-group col-md-6 mb-0'
                ),
                css_class='form-row'
            ),
            'notes',
            Div(
                HTML('<h4 class="mt-4">Payment Options</h4>'),
                'use_subscription',
                id='subscription_options',
                css_class='mt-4'
            ),
            Div(
                Submit('submit', 'Book Appointment', css_class='btn btn-primary btn-lg mt-3'),
                css_class='text-center mt-4'
            )
        )
        
        # Check if user has an active subscription
        self.has_active_subscription = False
        if self.user and self.user.is_authenticated:
            from booking.models import Subscription
            active_subscription = Subscription.objects.filter(
                user=self.user,
                status='active',
                end_date__gt=timezone.now(),
                sessions_remaining__gt=0
            ).first()
            
            if active_subscription:
                self.has_active_subscription = True
                self.fields['use_subscription'].help_text = f"You have {active_subscription.sessions_remaining} sessions remaining in your {active_subscription.plan.name} plan"
            else:
                self.fields['use_subscription'].widget = forms.HiddenInput()
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.user:
            instance.user = self.user
        
        # Handle subscription usage
        if self.cleaned_data.get('use_subscription') and self.has_active_subscription:
            from booking.models import Subscription
            active_subscription = Subscription.objects.filter(
                user=self.user,
                status='active',
                end_date__gt=timezone.now(),
                sessions_remaining__gt=0
            ).first()
            
            if active_subscription:
                instance.subscription = active_subscription
                instance.is_paid = True
                
                # Reduce the sessions remaining
                if commit:
                    active_subscription.sessions_remaining -= 1
                    active_subscription.save()
        
        if commit:
            instance.save()
        
        return instance