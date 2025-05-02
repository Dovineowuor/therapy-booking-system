document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const dateInput = document.getElementById('id_date');
    const therapistSelect = document.getElementById('id_therapist');
    const timeSlotsContainer = document.getElementById('time_slots');
    const timeSlotSelect = document.getElementById('id_time_slot');
    
    // Function to fetch available time slots
    function fetchTimeSlots() {
        const date = dateInput.value;
        const therapistId = therapistSelect.value;
        
        if (!date || !therapistId) {
            timeSlotsContainer.innerHTML = `
                <div class="alert alert-info">
                    Please select a date and therapist to see available time slots
                </div>
            `;
            return;
        }
        
        // Show loading indicator
        timeSlotsContainer.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading available time slots...</p>
            </div>
        `;
        
        // Fetch time slots from the server
        fetch(`/booking/get-time-slots/?date=${date}&therapist_id=${therapistId}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    timeSlotsContainer.innerHTML = `
                        <div class="alert alert-danger">
                            ${data.error}
                        </div>
                    `;
                    return;
                }
                
                if (data.time_slots.length === 0) {
                    timeSlotsContainer.innerHTML = `
                        <div class="alert alert-warning">
                            No time slots available for the selected date and therapist.
                            Please try another date or therapist.
                        </div>
                    `;
                    return;
                }
                
                // Render time slots as a select dropdown
                let html = '<select class="form-select" id="id_time_slot" name="time_slot">';
                html += '<option value="">Select a time slot</option>';
                data.time_slots.forEach(slot => {
                    html += `
                        <option value="${slot.id}">
                            ${slot.start_time} - ${slot.end_time}
                        </option>
                    `;
                });
                html += '</select>';
                
                timeSlotsContainer.innerHTML = html;
                
                // Add change event to time slot select
                const select = document.getElementById('id_time_slot');
                if (select) {
                    select.addEventListener('change', function() {
                        if (this.value) {
                            this.classList.add('is-valid');
                            this.classList.remove('is-invalid');
                        } else {
                            this.classList.remove('is-valid');
                            this.classList.add('is-invalid');
                        }
                    });
                }
            })
            .catch(error => {
                console.error('Error fetching time slots:', error);
                timeSlotsContainer.innerHTML = `
                    <div class="alert alert-danger">
                        An error occurred while fetching time slots. Please try again.
                    </div>
                `;
            });
    }
    
    // Add event listeners
    if (dateInput && therapistSelect) {
        dateInput.addEventListener('change', fetchTimeSlots);
        therapistSelect.addEventListener('change', fetchTimeSlots);
        
        // Initial fetch if both date and therapist are already selected
        if (dateInput.value && therapistSelect.value) {
            fetchTimeSlots();
        }
    }

    // Handle form submission
    const form = document.getElementById('booking-form');
    if (form) {
        form.addEventListener('submit', function(e) {
            // Get the selected time slot
            const timeSlotSelect = document.getElementById('id_time_slot');
            if (!timeSlotSelect.value) {
                e.preventDefault();
                alert('Please select a time slot before submitting');
                return false;
            }
            
            // Prevent the time slots from being fetched again
            dateInput.removeEventListener('change', fetchTimeSlots);
            therapistSelect.removeEventListener('change', fetchTimeSlots);
            
            // Allow the form to submit normally
            return true;
        });
    }
    
    // Handle subscription checkbox
    const useSubscriptionCheckbox = document.getElementById('id_use_subscription');
    if (useSubscriptionCheckbox) {
        useSubscriptionCheckbox.addEventListener('change', function() {
            // You can add logic here to update the UI based on whether the user wants to use their subscription
            // For example, show/hide payment options
        });
    }
});