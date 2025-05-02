from django import forms
from django.utils import timezone
from booking.models import MembershipPlan, Subscription, SubscriptionPayment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Div, HTML

class SubscriptionForm(forms.ModelForm):
    """Form for subscribing to a membership plan"""
    
    class Meta:
        model = Subscription
        fields = ['plan', 'auto_renew']
        widgets = {
            'auto_renew': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Only show active plans
        self.fields['plan'].queryset = MembershipPlan.objects.filter(is_active=True)
        
        # Customize the plan field to show more information
        self.fields['plan'].widget = forms.RadioSelect()
        self.fields['plan'].label = "Select a Membership Plan"
        
        # Set up crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4">Choose Your Membership Plan</h3>'),
            'plan',
            Div(
                HTML('<h4 class="mt-4 mb-3">Payment Options</h4>'),
                'auto_renew',
                css_class='mt-4'
            ),
            Div(
                Submit('submit', 'Subscribe Now', css_class='btn btn-primary btn-lg mt-3'),
                css_class='text-center mt-4'
            )
        )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user
        
        if commit:
            instance.save()
        return instance

class PaymentForm(forms.ModelForm):
    """Form for processing subscription payments"""
    
    card_number = forms.CharField(max_length=19, label="Card Number", 
                                 widget=forms.TextInput(attrs={'placeholder': '1234 5678 9012 3456'}))
    card_expiry = forms.CharField(max_length=5, label="Expiry Date (MM/YY)", 
                                 widget=forms.TextInput(attrs={'placeholder': 'MM/YY'}))
    card_cvc = forms.CharField(max_length=4, label="CVC", 
                              widget=forms.TextInput(attrs={'placeholder': '123'}))
    cardholder_name = forms.CharField(max_length=100, label="Cardholder Name",
                                     widget=forms.TextInput(attrs={'placeholder': 'John Doe'}))
    
    class Meta:
        model = SubscriptionPayment
        fields = ['payment_method']
        widgets = {
            'payment_method': forms.Select(choices=[
                ('credit_card', 'Credit Card'),
                ('paypal', 'PayPal'),
                ('bank_transfer', 'Bank Transfer')
            ])
        }
    
    def __init__(self, *args, **kwargs):
        self.subscription = kwargs.pop('subscription', None)
        super().__init__(*args, **kwargs)
        
        # Set up crispy forms
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            HTML('<h3 class="mb-4">Payment Details</h3>'),
            HTML('<div class="alert alert-info">You will be charged <strong>${{ amount }}</strong> for the {{ plan_name }} plan.</div>'),
            'payment_method',
            Div(
                HTML('<div id="credit_card_fields" class="mt-3">'),
                Row(
                    Column('cardholder_name', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('card_number', css_class='form-group col-md-12 mb-0'),
                    css_class='form-row'
                ),
                Row(
                    Column('card_expiry', css_class='form-group col-md-6 mb-0'),
                    Column('card_cvc', css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                HTML('</div>'),
                css_class='mt-3'
            ),
            Div(
                Submit('submit', 'Complete Payment', css_class='btn btn-success btn-lg mt-3'),
                css_class='text-center mt-4'
            )
        )
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        
        if self.subscription:
            instance.subscription = self.subscription
            instance.amount = self.subscription.plan.price
        
        # In a real application, you would process the payment here
        # For this demo, we'll just mark it as completed
        instance.status = 'completed'
        instance.transaction_id = f"DEMO-{timezone.now().strftime('%Y%m%d%H%M%S')}"
        
        if commit:
            instance.save()
            
            # Update the subscription status
            if self.subscription:
                self.subscription.status = 'active'
                self.subscription.save()
                
        return instance