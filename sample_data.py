import os
import django
import random
from datetime import datetime, timedelta, time
from decimal import Decimal

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapy_project.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from booking.models.booking import TherapyService, Therapist, TimeSlot, Booking
from booking.models.membership import MembershipPlan, Subscription, SubscriptionPayment

# Create sample users
def create_users():
    print("Creating users...")
    
    # Create admin user if it doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        print(f"Created admin user: {admin.username}")
    
    # Create regular users
    users = []
    for i in range(1, 6):
        user, created = User.objects.get_or_create(
            username=f'user{i}',
            defaults={
                'email': f'user{i}@example.com',
                'first_name': f'User{i}',
                'last_name': f'Lastname{i}'
            }
        )
        
        if created:
            user.set_password(f'userpassword{i}')
            user.save()
            print(f"Created user: {user.username}")
        else:
            print(f"User already exists: {user.username}")
            
        users.append(user)
    
    return users

# Create services
def create_services():
    print("Creating services...")
    
    services_data = [
        {
            'name': 'Individual Therapy',
            'description': 'One-on-one therapy sessions tailored to your specific needs and goals. Our therapists use evidence-based approaches to help you address challenges, develop coping strategies, and improve your overall well-being.',
            'duration': 50,
            'price': Decimal('120.00'),
        },
        {
            'name': 'Couples Therapy',
            'description': 'Therapy for couples looking to improve their relationship, resolve conflicts, and build stronger communication. Our therapists provide a safe space for both partners to express themselves and work toward mutual understanding.',
            'duration': 80,
            'price': Decimal('150.00'),
        },
        {
            'name': 'Family Therapy',
            'description': 'Sessions designed to address family dynamics, improve communication, and resolve conflicts within the family system. Our therapists work with all family members to create positive change and strengthen relationships.',
            'duration': 90,
            'price': Decimal('180.00'),
        },
        {
            'name': 'Anxiety Management',
            'description': 'Specialized therapy focused on managing anxiety symptoms and developing effective coping strategies. Learn techniques to reduce anxiety and regain control over your thoughts and feelings.',
            'duration': 50,
            'price': Decimal('130.00'),
        },
        {
            'name': 'Depression Treatment',
            'description': 'Therapy specifically designed to address depression symptoms and improve mood. Our therapists use evidence-based approaches to help you develop coping skills and work toward recovery.',
            'duration': 50,
            'price': Decimal('130.00'),
        },
        {
            'name': 'Stress Management',
            'description': 'Learn effective techniques to manage stress and prevent burnout. Our therapists will help you identify sources of stress and develop personalized strategies to improve your resilience and well-being.',
            'duration': 50,
            'price': Decimal('110.00'),
        },
    ]
    
    services = []
    for service_data in services_data:
        service, created = TherapyService.objects.get_or_create(
            name=service_data['name'],
            defaults=service_data
        )
        services.append(service)
        if created:
            print(f"Created service: {service.name}")
        else:
            print(f"Service already exists: {service.name}")
    
    return services

# Create therapists
def create_therapists():
    print("Creating therapists...")
    
    therapists_data = [
        {
            'first_name': 'Sarah',
            'last_name': 'Johnson',
            'bio': 'Dr. Johnson is a licensed clinical psychologist with over 15 years of experience. She specializes in cognitive-behavioral therapy and has helped hundreds of clients overcome anxiety, depression, and trauma. Her compassionate approach creates a safe space for clients to explore their challenges and work toward positive change.',
            'specialization': 'Anxiety, Depression, Trauma, CBT',
            'experience_years': 15,
        },
        {
            'first_name': 'Michael',
            'last_name': 'Rodriguez',
            'bio': 'Michael is a licensed marriage and family therapist with expertise in relationship dynamics and family systems. He helps couples and families improve communication, resolve conflicts, and build stronger connections. His warm and engaging style helps clients feel comfortable discussing sensitive issues.',
            'specialization': 'Couples Therapy, Family Therapy, Relationship Issues',
            'experience_years': 10,
        },
        {
            'first_name': 'Emily',
            'last_name': 'Chen',
            'bio': 'Dr. Chen combines traditional psychotherapy with mindfulness-based approaches to help clients manage stress, anxiety, and life transitions. She believes in treating the whole person and works collaboratively with clients to develop personalized treatment plans that address their unique needs and goals.',
            'specialization': 'Mindfulness, Stress Management, Life Transitions, Anxiety',
            'experience_years': 12,
        },
        {
            'first_name': 'James',
            'last_name': 'Wilson',
            'bio': 'James specializes in helping clients navigate life challenges, trauma, and mental health concerns. With a background in social work, he brings a unique perspective that considers environmental and social factors affecting mental health. His approach is strengths-based and solution-focused.',
            'specialization': 'Trauma, PTSD, Depression, Grief',
            'experience_years': 8,
        },
        {
            'first_name': 'Olivia',
            'last_name': 'Thompson',
            'bio': 'Dr. Thompson specializes in working with children and adolescents facing emotional and behavioral challenges. She uses play therapy, cognitive-behavioral techniques, and family systems approaches to help young clients develop coping skills and improve their emotional well-being.',
            'specialization': 'Child Psychology, Adolescent Therapy, ADHD, Behavioral Issues',
            'experience_years': 14,
        },
    ]
    
    therapists = []
    for therapist_data in therapists_data:
        # Create a user for the therapist
        first_name = therapist_data.pop('first_name')
        last_name = therapist_data.pop('last_name')
        username = f"{first_name.lower()}.{last_name.lower()}"
        email = f"{username}@example.com"
        
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
                'is_staff': True
            }
        )
        
        if created:
            user.set_password(f"password{first_name.lower()}")
            user.save()
            print(f"Created user for therapist: {user.username}")
        
        # Create the therapist profile
        therapist, created = Therapist.objects.get_or_create(
            user=user,
            defaults=therapist_data
        )
        
        therapists.append(therapist)
        if created:
            print(f"Created therapist: {therapist}")
        else:
            print(f"Therapist already exists: {therapist}")
    
    return therapists

# Create time slots
def create_time_slots(therapists):
    print("Creating time slots...")
    
    # Clear existing future time slots
    future_slots = TimeSlot.objects.filter(date__gte=datetime.now().date())
    future_slots.delete()
    
    time_slots = []
    
    # Create time slots for the next 14 days
    for day in range(14):
        slot_date = datetime.now().date() + timedelta(days=day)
        
        # Skip weekends
        if slot_date.weekday() >= 5:  # 5 = Saturday, 6 = Sunday
            continue
        
        # Create slots for each therapist
        for therapist in therapists:
            # Morning slots
            start_times = [
                time(9, 0), time(10, 0), time(11, 0),  # Morning slots
                time(13, 0), time(14, 0), time(15, 0), time(16, 0), time(17, 0)  # Afternoon slots
            ]
            
            for start_time in start_times:
                # Randomly make some slots unavailable
                if random.random() < 0.3:  # 30% chance of being unavailable
                    continue
                
                # Calculate end time (50 minutes later)
                end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=50)).time()
                
                time_slot = TimeSlot.objects.create(
                    therapist=therapist,
                    date=slot_date,
                    start_time=start_time,
                    end_time=end_time,
                    is_available=True
                )
                time_slots.append(time_slot)
                print(f"Created time slot: {time_slot.date} {time_slot.start_time}-{time_slot.end_time} with {therapist}")
    
    return time_slots

# Create membership plans
def create_membership_plans():
    print("Creating membership plans...")
    
    plans_data = [
        {
            'name': 'Basic Plan',
            'slug': 'basic-plan',
            'description': 'Perfect for occasional therapy needs. Includes 4 sessions per month at a discounted rate.',
            'price': Decimal('399.00'),
            'duration_days': 30,
            'sessions_included': 4,
            'features': 'Discounted session rate,Priority booking,Email support',
        },
        {
            'name': 'Standard Plan',
            'slug': 'standard-plan',
            'description': 'Our most popular plan. Includes 8 sessions per month, perfect for regular therapy.',
            'price': Decimal('699.00'),
            'duration_days': 30,
            'sessions_included': 8,
            'features': 'Discounted session rate,Priority booking,Email support,Phone support,Wellness resources',
        },
        {
            'name': 'Premium Plan',
            'slug': 'premium-plan',
            'description': 'Comprehensive therapy support with unlimited sessions for those who need intensive care.',
            'price': Decimal('999.00'),
            'duration_days': 30,
            'sessions_included': 12,
            'features': 'Unlimited sessions,Priority booking,24/7 support,Wellness resources,Monthly progress report,Emergency sessions',
        },
    ]
    
    plans = []
    for plan_data in plans_data:
        plan, created = MembershipPlan.objects.get_or_create(
            name=plan_data['name'],
            defaults=plan_data
        )
        plans.append(plan)
        if created:
            print(f"Created membership plan: {plan.name}")
        else:
            print(f"Membership plan already exists: {plan.name}")
    
    return plans

# Create subscriptions for users
def create_subscriptions(users, plans):
    print("Creating subscriptions...")
    
    subscriptions = []
    
    # Assign random plans to users
    for i, user in enumerate(users):
        # Skip some users to have non-subscribed users
        if i % 3 == 0:
            continue
        
        plan = random.choice(plans)
        
        # Create subscription
        start_date = datetime.now().date() - timedelta(days=random.randint(1, 15))
        end_date = start_date + timedelta(days=plan.duration_days)
        
        subscription = Subscription.objects.create(
            user=user,
            plan=plan,
            start_date=start_date,
            end_date=end_date,
            status='active',
            sessions_remaining=plan.sessions_included - random.randint(0, 3)
        )
        
        # Create payment for subscription
        payment = SubscriptionPayment.objects.create(
            subscription=subscription,
            amount=plan.price,
            payment_date=start_date,
            payment_method='Credit Card',
            transaction_id=f'txn_{random.randint(100000, 999999)}'
        )
        
        subscriptions.append(subscription)
        print(f"Created subscription for {user.username}: {plan.name}")
        print(f"Created payment: ${payment.amount}")
    
    return subscriptions

# Create bookings
def create_bookings(users, services, time_slots, subscriptions):
    print("Creating bookings...")
    
    bookings = []
    
    # Create past bookings
    for i in range(10):
        user = random.choice(users)
        service = random.choice(services)
        
        # Find a therapist who offers this service
        therapist = random.choice(Therapist.objects.all())
        
        # Create a past time slot
        past_date = datetime.now().date() - timedelta(days=random.randint(1, 30))
        start_time = time(random.randint(9, 17), 0)
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(minutes=service.duration)).time()
        
        past_slot = TimeSlot.objects.create(
            therapist=therapist,
            date=past_date,
            start_time=start_time,
            end_time=end_time,
            is_available=False
        )
        
        # Check if user has subscription
        user_subscription = None
        for subscription in subscriptions:
            if subscription.user == user:
                user_subscription = subscription
                break
        
        booking = Booking.objects.create(
            client=user,
            service=service,
            therapist=therapist,
            time_slot=past_slot,
            status='completed',
            notes=f"Past booking for {service.name}",
            subscription=user_subscription
        )
        
        if user_subscription and booking.status == 'completed':
            # Deduct a session if it was used
            if user_subscription.sessions_remaining > 0:
                user_subscription.sessions_remaining -= 1
                user_subscription.save()
        
        bookings.append(booking)
        print(f"Created past booking: {booking.service.name} on {booking.time_slot.date}")
    
    # Create future bookings
    available_slots = [slot for slot in time_slots if slot.is_available]
    
    for i in range(min(15, len(available_slots))):
        user = random.choice(users)
        service = random.choice(services)
        slot = available_slots[i]
        
        # Check if user has subscription
        user_subscription = None
        for subscription in subscriptions:
            if subscription.user == user and subscription.is_active():
                user_subscription = subscription
                break
        
        booking = Booking.objects.create(
            client=user,
            service=service,
            therapist=slot.therapist,
            time_slot=slot,
            status='confirmed',
            notes=f"Future booking for {service.name}",
            subscription=user_subscription
        )
        
        # Mark slot as unavailable
        slot.is_available = False
        slot.save()
        
        bookings.append(booking)
        print(f"Created future booking: {booking.service.name} on {booking.time_slot.date}")
    
    return bookings

# Main function to create all sample data
def create_sample_data():
    print("Creating sample data...")
    
    users = create_users()
    services = create_services()
    therapists = create_therapists()
    time_slots = create_time_slots(therapists)
    plans = create_membership_plans()
    subscriptions = create_subscriptions(users, plans)
    bookings = create_bookings(users, services, time_slots, subscriptions)
    
    print("\nSample data creation complete!")
    print(f"Created {len(users)} users")
    print(f"Created {len(services)} services")
    print(f"Created {len(therapists)} therapists")
    print(f"Created {len(time_slots)} time slots")
    print(f"Created {len(plans)} membership plans")
    print(f"Created {len(subscriptions)} subscriptions")
    print(f"Created {len(bookings)} bookings")
    
    print("\nYou can log in with the following credentials:")
    print("Admin: username=admin, password=adminpassword")
    for i in range(1, 6):
        print(f"User {i}: username=user{i}, password=userpassword{i}")

if __name__ == '__main__':
    create_sample_data()