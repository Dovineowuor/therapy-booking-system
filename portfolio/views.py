from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Project, Testimonial, Career
from .forms import ContactForm
from django.views import generic

class ProjectListView(generic.ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 6

    def get_queryset(self):
        return Project.objects.order_by('-created_at')

class ProjectDetailView(generic.DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'
    slug_url_kwarg = 'slug'
    slug_field = 'slug'

class TestimonialListView(generic.ListView):
    model = Testimonial
    template_name = 'portfolio/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 6

    def get_queryset(self):
        return Testimonial.objects.filter(is_active=True).order_by('-created_at')

class CareerListView(generic.ListView):
    model = Career
    template_name = 'portfolio/careers.html'
    context_object_name = 'careers'
    paginate_by = 6

    def get_queryset(self):
        return Career.objects.filter(is_active=True).order_by('-created_at')

class CareerDetailView(generic.DetailView):
    model = Career
    template_name = 'portfolio/career_detail.html'
    context_object_name = 'career'

    def get_queryset(self):
        return Career.objects.filter(is_active=True)

def portfolio(request):
    """Main portfolio page with featured projects"""
    featured_projects = Project.objects.filter(is_featured=True)
    categories = Category.objects.all()
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    
    context = {
        'featured_projects': featured_projects,
        'categories': categories,
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/portfolio.html', context)

def project_list(request):
    """List all projects, optionally filtered by category"""
    category_slug = request.GET.get('category')
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        projects = Project.objects.filter(category=category)
        title = f"Projects in {category.name}"
    else:
        projects = Project.objects.all()
        title = "All Projects"
    
    categories = Category.objects.all()
    
    context = {
        'projects': projects,
        'categories': categories,
        'title': title,
        'current_category': category_slug,
    }
    return render(request, 'portfolio/project_list.html', context)

def project_detail(request, slug):
    """Show details of a specific project"""
    project = get_object_or_404(Project, slug=slug)
    related_projects = Project.objects.filter(category=project.category).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'portfolio/project_detail.html', context)

def testimonials(request):
    """View all testimonials"""
    testimonials = Testimonial.objects.filter(is_active=True)
    
    context = {
        'testimonials': testimonials,
    }
    return render(request, 'portfolio/testimonials.html', context)

def about(request):
    about_page = About.objects.first()
    context = {
        'about': about_page
    }
    return render(request, 'portfolio/about.html', context)

def career(request):
    """View all careers"""
    careers = Career.objects.filter(is_active=True)
    
    context = {
        'careers': careers,
    }
    return render(request, 'portfolio/careers.html', context)

def career_detail(request, slug):
    """Show details of a specific career"""
    career = get_object_or_404(Career, slug=slug)
    
    context = {
        'career': career,
    }
    return render(request, 'portfolio/career_detail.html', context)

def blog(request):
    """View all blogs"""
    blogs = Blog.objects.filter(is_active=True)
    
    context = {
        'blogs': blogs,
    }
    return render(request, 'portfolio/blog.html', context)

def blog_detail(request, slug):
    """Show details of a specific blog"""
    blog = get_object_or_404(Blog, slug=slug)
    
    context = {
        'blog': blog,
    }
    return render(request, 'portfolio/blog_detail.html', context)

def contact(request):
    """Contact form page"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Send email
            subject = f'New Contact Form Submission - {form.cleaned_data["name"]}'
            message = f"Name: {form.cleaned_data['name']}\n"
            message += f"Email: {form.cleaned_data['email']}\n"
            message += f"Subject: {form.cleaned_data['subject']}\n"
            message += f"Message: {form.cleaned_data['message']}"
            
            try:
                send_mail(
                    subject,
                    message,
                    form.cleaned_data['email'],
                    [settings.DEFAULT_FROM_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Your message has been sent successfully!')
            except Exception as e:
                messages.error(request, 'There was an error sending your message. Please try again later.')
                print(f"Error sending email: {e}")

            return redirect('portfolio:contact')
    else:
        form = ContactForm()

    return render(request, 'portfolio/contact.html', {'form': form})
