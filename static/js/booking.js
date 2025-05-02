document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const dateInput = document.getElementById('id_date');
    const therapistSelect = document.getElementById('id_therapist');
    const timeSlotsContainer = document.getElementById('time_slots');
    const timeSlotInput = document.getElementById('id_time_slot');
    
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
                
                // Render time slots
                let html = '<div class="time-slots-grid">';
                data.time_slots.forEach(slot => {
                    html += `
                        <div class="time-slot" data-id="${slot.id}">
                            ${slot.start_time} - ${slot.end_time}
                        </div>
                    `;
                });
                html += '</div>';
                
                timeSlotsContainer.innerHTML = html;
                
                // Add click event to time slots
                document.querySelectorAll('.time-slot').forEach(slot => {
                    slot.addEventListener('click', function() {
                        // Remove selected class from all time slots
                        document.querySelectorAll('.time-slot').forEach(s => {
                            s.classList.remove('selected');
                        });
                        
                        // Add selected class to this time slot
                        this.classList.add('selected');
                        
                        // Set the time slot ID in the hidden input
                        timeSlotInput.value = this.dataset.id;
                    });
                });
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
    
    // Handle subscription checkbox
    const useSubscriptionCheckbox = document.getElementById('id_use_subscription');
    if (useSubscriptionCheckbox) {
        useSubscriptionCheckbox.addEventListener('change', function() {
            // You can add logic here to update the UI based on whether the user wants to use their subscription
            // For example, show/hide payment options
        });
    }
});