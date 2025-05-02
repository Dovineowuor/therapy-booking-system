import os
import django
import datetime
from django.utils.text import slugify

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'therapy_project.settings')
django.setup()

from portfolio.models import Category, Project, ProjectImage, Testimonial

def create_sample_data():
    print("Creating portfolio sample data...")
    
    # Create categories
    categories = create_categories()
    
    # Create projects
    projects = create_projects(categories)
    
    # Create project images
    project_images = create_project_images(projects)
    
    # Create testimonials
    testimonials = create_testimonials()
    
    print("\nPortfolio sample data creation complete!")
    print(f"Created {len(categories)} categories")
    print(f"Created {len(projects)} projects")
    print(f"Created {len(project_images)} project images")
    print(f"Created {len(testimonials)} testimonials")

def create_categories():
    categories_data = [
        {
            'name': 'Individual Therapy',
            'description': 'Our individual therapy services focus on personal growth and addressing specific mental health concerns.'
        },
        {
            'name': 'Couples Therapy',
            'description': 'Our couples therapy services help partners improve communication and resolve conflicts.'
        },
        {
            'name': 'Family Therapy',
            'description': 'Our family therapy services address family dynamics and improve relationships between family members.'
        },
        {
            'name': 'Specialized Programs',
            'description': 'Our specialized programs target specific mental health concerns like anxiety, depression, and stress management.'
        },
        {
            'name': 'Workshops',
            'description': 'Our workshops provide group learning experiences on various mental health and wellness topics.'
        }
    ]
    
    categories = []
    for category_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=category_data['name'],
            defaults={
                'slug': slugify(category_data['name']),
                'description': category_data['description']
            }
        )
        
        if created:
            print(f"Created category: {category.name}")
        else:
            print(f"Category already exists: {category.name}")
        
        categories.append(category)
    
    return categories

def create_projects(categories):
    projects_data = [
        {
            'title': 'Anxiety Management Program',
            'description': 'A comprehensive 8-week program designed to help clients manage anxiety through cognitive-behavioral techniques, mindfulness practices, and stress reduction strategies. This program has shown significant results in reducing anxiety symptoms and improving overall quality of life for participants.',
            'category': 'Specialized Programs',
            'client': 'Community Mental Health Center',
            'date_completed': datetime.date(2025, 3, 15),
            'is_featured': True
        },
        {
            'title': 'Couples Communication Workshop',
            'description': 'A weekend workshop focused on improving communication skills for couples. Participants learn active listening techniques, conflict resolution strategies, and ways to express needs effectively. This workshop has helped numerous couples strengthen their relationships and develop healthier communication patterns.',
            'category': 'Couples Therapy',
            'client': 'Relationship Counseling Center',
            'date_completed': datetime.date(2025, 2, 28),
            'is_featured': True
        },
        {
            'title': 'Family Reconciliation Project',
            'description': 'A specialized therapy program designed to help estranged family members rebuild relationships and heal past wounds. This project involves individual and group sessions, structured communication exercises, and guided reconciliation activities. The program has successfully reunited families and established healthier family dynamics.',
            'category': 'Family Therapy',
            'client': 'Family Support Services',
            'date_completed': datetime.date(2025, 1, 20),
            'is_featured': True
        },
        {
            'title': 'Mindfulness for Depression',
            'description': 'A 10-week program integrating mindfulness practices with cognitive therapy to address depression. Participants learn to observe thoughts without judgment, develop present-moment awareness, and cultivate self-compassion. This program has shown effectiveness in reducing depressive symptoms and preventing relapse.',
            'category': 'Specialized Programs',
            'client': 'Wellness Center',
            'date_completed': datetime.date(2024, 12, 10),
            'is_featured': False
        },
        {
            'title': 'Grief Support Group',
            'description': 'A supportive therapy group for individuals experiencing grief and loss. The group provides a safe space for expressing emotions, sharing experiences, and learning coping strategies. Participants develop connections with others going through similar experiences and find comfort in shared healing.',
            'category': 'Individual Therapy',
            'client': 'Bereavement Support Network',
            'date_completed': datetime.date(2024, 11, 5),
            'is_featured': False
        },
        {
            'title': 'Stress Management for Professionals',
            'description': 'A corporate workshop series designed to help professionals manage workplace stress and prevent burnout. The program includes stress assessment, relaxation techniques, time management strategies, and work-life balance planning. Participating organizations have reported improved employee well-being and productivity.',
            'category': 'Workshops',
            'client': 'Corporate Wellness Program',
            'date_completed': datetime.date(2025, 4, 1),
            'is_featured': True
        },
        {
            'title': 'Parenting Skills Workshop',
            'description': 'A series of workshops for parents focusing on effective communication, setting boundaries, positive discipline, and nurturing emotional intelligence in children. Parents learn practical strategies to strengthen their relationship with their children and create a supportive family environment.',
            'category': 'Family Therapy',
            'client': 'Community Family Center',
            'date_completed': datetime.date(2024, 10, 15),
            'is_featured': False
        },
        {
            'title': 'Trauma Recovery Program',
            'description': 'A specialized therapy program for individuals recovering from trauma. The program integrates evidence-based approaches including EMDR, somatic experiencing, and narrative therapy. Participants work through traumatic experiences in a safe, supportive environment and develop resilience and coping skills.',
            'category': 'Individual Therapy',
            'client': 'Trauma Recovery Center',
            'date_completed': datetime.date(2025, 3, 30),
            'is_featured': True
        }
    ]
    
    projects = []
    for project_data in projects_data:
        # Find the category
        category_name = project_data['category']
        category = next((c for c in categories if c.name == category_name), None)
        
        if not category:
            print(f"Category not found: {category_name}")
            continue
        
        project, created = Project.objects.get_or_create(
            title=project_data['title'],
            defaults={
                'slug': slugify(project_data['title']),
                'description': project_data['description'],
                'category': category,
                'client': project_data['client'],
                'date_completed': project_data['date_completed'],
                'is_featured': project_data['is_featured'],
                # Note: In a real application, you would handle image uploads differently
                # For this sample, we're not setting images
            }
        )
        
        if created:
            print(f"Created project: {project.title}")
        else:
            print(f"Project already exists: {project.title}")
        
        projects.append(project)
    
    return projects

def create_project_images(projects):
    # In a real application, you would handle actual image uploads
    # For this sample, we're just creating the database entries without actual images
    
    project_images = []
    for project in projects:
        # Create 3 sample images for each project
        for i in range(1, 4):
            image, created = ProjectImage.objects.get_or_create(
                project=project,
                caption=f"Image {i} for {project.title}",
                order=i
                # Note: In a real application, you would handle image uploads differently
            )
            
            if created:
                print(f"Created project image: {image.caption}")
            else:
                print(f"Project image already exists: {image.caption}")
            
            project_images.append(image)
    
    return project_images

def create_testimonials():
    testimonials_data = [
        {
            'name': 'Jennifer Smith',
            'position': 'Marketing Director',
            'company': 'ABC Corporation',
            'quote': 'The anxiety management program completely transformed my life. I\'ve learned valuable techniques to manage my anxiety and feel more in control. The therapists were compassionate, knowledgeable, and truly invested in my well-being.'
        },
        {
            'name': 'Michael Johnson',
            'position': 'Software Engineer',
            'company': 'Tech Innovations',
            'quote': 'My wife and I participated in the couples communication workshop, and it was a game-changer for our relationship. We now have the tools to communicate effectively and resolve conflicts in a healthy way. I highly recommend this to any couple looking to strengthen their relationship.'
        },
        {
            'name': 'Sarah Williams',
            'position': 'Teacher',
            'company': 'Oakwood Elementary',
            'quote': 'The family therapy sessions helped us navigate a difficult time and rebuild our relationships. Our therapist created a safe space for everyone to express themselves and guided us toward healing. We\'re now a stronger, more connected family.'
        },
        {
            'name': 'David Chen',
            'position': 'Financial Analyst',
            'company': 'Global Investments',
            'quote': 'The stress management workshop provided practical strategies that I use daily in my high-pressure job. I\'ve seen significant improvements in my work-life balance and overall well-being. The techniques are simple yet incredibly effective.'
        },
        {
            'name': 'Emily Rodriguez',
            'position': 'Healthcare Worker',
            'company': 'City Hospital',
            'quote': 'After struggling with depression for years, the mindfulness program gave me a new perspective and effective tools for managing my symptoms. The therapists were supportive and knowledgeable, and the group setting provided valuable connections with others on similar journeys.'
        },
        {
            'name': 'Robert Taylor',
            'position': 'Business Owner',
            'company': 'Taylor Enterprises',
            'quote': 'The parenting workshop transformed my relationship with my teenagers. I learned how to communicate more effectively and set appropriate boundaries while maintaining a loving connection. Our home is now more peaceful and our relationships are stronger.'
        }
    ]
    
    testimonials = []
    for testimonial_data in testimonials_data:
        testimonial, created = Testimonial.objects.get_or_create(
            name=testimonial_data['name'],
            defaults={
                'position': testimonial_data['position'],
                'company': testimonial_data['company'],
                'quote': testimonial_data['quote'],
                'is_active': True
                # Note: In a real application, you would handle image uploads differently
            }
        )
        
        if created:
            print(f"Created testimonial from: {testimonial.name}")
        else:
            print(f"Testimonial already exists from: {testimonial.name}")
        
        testimonials.append(testimonial)
    
    return testimonials

if __name__ == '__main__':
    create_sample_data()