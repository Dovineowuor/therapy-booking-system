from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Category, Project, Testimonial
from .forms import ContactForm

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

def contact(request):
    """Contact form view"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email (commented out for now as we don't have email settings)
            # send_mail(
            #     f"Contact Form: {subject}",
            #     f"From: {name} <{email}>\n\n{message}",
            #     settings.DEFAULT_FROM_EMAIL,
            #     [settings.CONTACT_EMAIL],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('portfolio:contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'portfolio/contact.html', context)
