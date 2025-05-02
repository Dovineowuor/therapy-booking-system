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

### Quick Setup

For a quick setup, you can use the provided setup script:

```bash
# Make the script executable
chmod +x setup_project.sh

# Run the setup script
./setup_project.sh
```

This script will:
1. Create a virtual environment
2. Install dependencies
3. Apply migrations
4. Create a superuser
5. Load sample data
6. Start the development server

### Manual Setup

If you prefer to set up manually:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/therapy_booking.git
   cd therapy_booking
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Load sample data (optional):
   ```bash
   python sample_data.py
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the application at http://127.0.0.1:8000/

### GitHub Repository Setup

To push this project to your own GitHub repository:

1. Create a new repository on GitHub named `therapy-booking-system` (or your preferred name)

2. Use the provided script to set up the remote:
   ```bash
   # Make the script executable
   chmod +x setup_github.sh
   
   # Run the script with your GitHub username
   ./setup_github.sh your_github_username [optional_repository_name]
   ```

3. Push the code to your repository:
   ```bash
   git push -u origin main
   ```

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