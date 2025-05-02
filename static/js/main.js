// Main JavaScript file for Therapy Booking website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Time slot selection
    const timeSlots = document.querySelectorAll('.time-slot:not(.unavailable)');
    if (timeSlots.length > 0) {
        timeSlots.forEach(slot => {
            slot.addEventListener('click', function() {
                // Remove selected class from all slots
                timeSlots.forEach(s => s.classList.remove('selected'));
                // Add selected class to clicked slot
                this.classList.add('selected');
                // Update hidden input with selected time
                document.getElementById('selected_time').value = this.dataset.time;
            });
        });
    }

    // Date picker initialization for booking form
    const dateInput = document.getElementById('booking_date');
    if (dateInput) {
        dateInput.addEventListener('change', function() {
            // You could add AJAX call here to fetch available time slots for the selected date
            console.log('Date selected:', this.value);
        });
    }

    // Form validation
    const forms = document.querySelectorAll('.needs-validation');
    if (forms.length > 0) {
        Array.from(forms).forEach(form => {
            form.addEventListener('submit', event => {
                if (!form.checkValidity()) {
                    event.preventDefault();
                    event.stopPropagation();
                }
                form.classList.add('was-validated');
            }, false);
        });
    }
});