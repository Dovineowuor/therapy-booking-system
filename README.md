# Therapy Booking System

A comprehensive web application for therapy booking management and portfolio showcase built with Django, Bootstrap, and Crispy Forms.

## Features

### Booking System
- Service browsing and details
- Therapist profiles and specialties
- Appointment scheduling with time slot selection
- Booking management (view, cancel, reschedule)
- Email notifications for bookings and reminders

### Membership System
- Subscription plans with different benefits
- Subscription management
- Payment processing
- Usage tracking

### Portfolio
- Therapist showcase
- Service descriptions
- Testimonials
- Contact form

## Technology Stack

- **Backend**: Django 5.2
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Form Handling**: django-crispy-forms with crispy-bootstrap5
- **Database**: SQLite (development) / PostgreSQL (production)
- **Image Handling**: Pillow

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/therapy_booking.git
   cd therapy_booking
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```
   python manage.py migrate
   ```

5. Create a superuser:
   ```
   python manage.py createsuperuser
   ```

6. Run the development server:
   ```
   python manage.py runserver
   ```

7. Access the application at http://127.0.0.1:8000/

## Project Structure

```
therapy_booking/
├── booking/                  # Booking app
│   ├── forms/                # Form definitions
│   ├── models/               # Model definitions
│   ├── templates/booking/    # Booking templates
│   ├── views/                # View definitions
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── urls.py               # URL routing
│   └── tests.py              # Tests
├── portfolio/                # Portfolio app
│   ├── templates/portfolio/  # Portfolio templates
│   ├── admin.py              # Admin configuration
│   ├── apps.py               # App configuration
│   ├── models.py             # Model definitions
│   ├── urls.py               # URL routing
│   └── views.py              # View definitions
├── static/                   # Static files
│   ├── css/                  # CSS files
│   ├── js/                   # JavaScript files
│   └── images/               # Image files
├── templates/                # Global templates
│   ├── base.html             # Base template
│   ├── home.html             # Homepage
│   └── ...                   # Other global templates
├── therapy_project/          # Project settings
│   ├── settings.py           # Project settings
│   ├── urls.py               # Project URL routing
│   └── wsgi.py               # WSGI configuration
├── manage.py                 # Django management script
└── requirements.txt          # Project dependencies
```

## Usage

### Admin Interface

Access the admin interface at http://127.0.0.1:8000/admin/ to:
- Manage services and therapists
- View and manage bookings
- Configure membership plans
- Manage user accounts

### Booking System

- Browse available services
- View therapist profiles
- Select a service and therapist
- Choose an available time slot
- Confirm booking
- Manage existing bookings

### Membership System

- View available membership plans
- Subscribe to a plan
- Process payment
- Use subscription benefits for bookings
- Manage subscription

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Django
- Bootstrap
- django-crispy-forms
- crispy-bootstrap5