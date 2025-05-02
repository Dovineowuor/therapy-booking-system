// JavaScript for the home page

document.addEventListener('DOMContentLoaded', function() {
    // Animate hero image on hover
    const heroImage = document.querySelector('.hero-section img');
    if (heroImage) {
        heroImage.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const xPercent = x / rect.width - 0.5;
            const yPercent = y / rect.height - 0.5;
            
            const rotateX = yPercent * 10; // Max 5 degrees rotation
            const rotateY = -xPercent * 10; // Max 5 degrees rotation
            
            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        
        heroImage.addEventListener('mouseleave', function() {
            this.style.transform = 'perspective(1000px) rotateY(-15deg)';
        });
    }
    
    // Testimonial carousel
    const testimonialSection = document.querySelector('.testimonials-section');
    if (testimonialSection) {
        const testimonialCarousel = new bootstrap.Carousel(testimonialSection.querySelector('.carousel'), {
            interval: 5000,
            wrap: true,
            touch: true
        });
    }
    
    // Animate service cards on scroll
    const serviceCards = document.querySelectorAll('.service-card');
    const animateServiceCards = function() {
        serviceCards.forEach((card, index) => {
            const cardPosition = card.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (cardPosition < windowHeight - 50) {
                setTimeout(() => {
                    card.classList.add('fade-in');
                }, index * 100); // Stagger the animations
            }
        });
    };
    
    window.addEventListener('scroll', animateServiceCards);
    animateServiceCards(); // Run once on page load
    
    // Membership plan selection
    const planButtons = document.querySelectorAll('.pricing-card .btn');
    planButtons.forEach(button => {
        button.addEventListener('click', function() {
            const planName = this.closest('.pricing-card').querySelector('h3').textContent.trim().toLowerCase();
            localStorage.setItem('selectedPlan', planName);
        });
    });
    
    // Animate numbers (statistics)
    const animateValue = (element, start, end, duration) => {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const value = Math.floor(progress * (end - start) + start);
            element.textContent = value.toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    };
    
    const statNumbers = document.querySelectorAll('.stat-number');
    const animateStats = function() {
        statNumbers.forEach(stat => {
            const statPosition = stat.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (statPosition < windowHeight - 50 && !stat.classList.contains('animated')) {
                stat.classList.add('animated');
                const endValue = parseInt(stat.getAttribute('data-value'), 10);
                animateValue(stat, 0, endValue, 2000);
            }
        });
    };
    
    window.addEventListener('scroll', animateStats);
    animateStats(); // Run once on page load
    
    // Parallax effect for CTA section
    const ctaSection = document.querySelector('.cta-section');
    if (ctaSection) {
        window.addEventListener('scroll', function() {
            const scrollPosition = window.pageYOffset;
            const ctaPosition = ctaSection.offsetTop;
            const distance = scrollPosition - ctaPosition;
            
            if (distance > -window.innerHeight && distance < ctaSection.offsetHeight) {
                const parallaxElements = ctaSection.querySelectorAll('.parallax');
                parallaxElements.forEach(element => {
                    const speed = element.getAttribute('data-speed') || 0.2;
                    element.style.transform = `translateY(${distance * speed}px)`;
                });
            }
        });
    }
});