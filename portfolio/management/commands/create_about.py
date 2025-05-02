from django.core.management.base import BaseCommand
from portfolio.models import About

class Command(BaseCommand):
    help = 'Creates the About page'

    def handle(self, *args, **options):
        # Create the About page
        about = About.objects.create(
            title="About Therapy Booking",
            content="""<p>Welcome to Therapy Booking, your trusted partner in mental health care. We are dedicated to providing accessible, professional, and compassionate therapy services to help individuals achieve their mental wellness goals.</p>""",
            mission_statement="""<p>Our mission is to make mental health care accessible and affordable to everyone, while maintaining the highest standards of professionalism and care.</p>""",
            vision_statement="""<p>We envision a world where mental health is prioritized and everyone has access to the support they need to thrive.</p>""",
            values="""<ul>
                <li><strong>Compassion:</strong> We approach every client with empathy and understanding.</li>
                <li><strong>Professionalism:</strong> We maintain the highest standards of care and confidentiality.</li>
                <li><strong>Accessibility:</strong> We strive to make mental health care accessible to all.</li>
                <li><strong>Quality:</strong> We provide exceptional care from experienced professionals.</li>
            </ul>""",
            history="""<p>Therapy Booking was founded in 2025 with a vision to revolutionize mental health care. Our team of experienced therapists has helped countless individuals on their journey to better mental health.</p>"""
        )
        self.stdout.write(self.style.SUCCESS('About page created successfully!'))
