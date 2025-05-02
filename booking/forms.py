from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Field, HTML, Div
from .models import Booking, Review, TherapyService, TimeSlot

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Register', css_class='btn btn-primary')
        )

class BookingForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    service = forms.ModelChoiceField(queryset=TherapyService.objects.filter(is_active=True))
    selected_time = forms.CharField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Booking
        fields = ['service', 'notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            'service',
            Field('date', css_class='mb-3'),
            HTML('<div id="time_slots_container" class="mb-3"><p>Select a date to view available time slots</p></div>'),
            'selected_time',
            'notes',
            Submit('submit', 'Book Appointment', css_class='btn btn-primary')
        )

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f"{i} Stars") for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Div(
                HTML('<p class="mb-2">How would you rate your experience?</p>'),
                Field('rating', template='booking/rating_field.html'),
                css_class='mb-3'
            ),
            Field('comment', placeholder='Share your experience...'),
            Submit('submit', 'Submit Review', css_class='btn btn-primary')
        )