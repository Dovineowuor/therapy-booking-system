from django.db import models
from django.utils.text import slugify
from froala_editor.fields import FroalaField

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='projects')
    image = models.ImageField(upload_to='portfolio/')
    client = models.CharField(max_length=100, blank=True, null=True)
    date_completed = models.DateField()
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_completed']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio/gallery/')
    caption = models.CharField(max_length=200, blank=True, null=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"Image for {self.project.title}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True, null=True)
    company = models.CharField(max_length=100, blank=True, null=True)
    quote = models.TextField()
    image = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Testimonial from {self.name}"

class Career(models.Model):
    DEPARTMENT_CHOICES = [
        ('THERAPY', 'Therapy Services'),
        ('ADMIN', 'Administration'),
        ('IT', 'Information Technology'),
        ('HR', 'Human Resources'),
        ('MARKETING', 'Marketing'),
        ('FINANCE', 'Finance'),
    ]

    JOB_TYPE_CHOICES = [
        ('FULL_TIME', 'Full-time'),
        ('PART_TIME', 'Part-time'),
        ('CONTRACT', 'Contract'),
    ]

    title = models.CharField(max_length=200)
    department = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    location = models.CharField(max_length=100)
    is_remote = models.BooleanField(default=False)
    salary_range = models.CharField(max_length=100, blank=True)
    experience_required = models.CharField(max_length=50, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job Position'
        verbose_name_plural = 'Job Positions'

    def __str__(self):
        return f"{self.title} - {self.get_department_display()}"

    def get_absolute_url(self):
        return reverse('portfolio:career_detail', kwargs={'slug': self.slug})
        
class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    mission_statement = models.TextField()
    vision_statement = models.TextField()
    values = models.TextField()
    history = models.TextField()
    image = models.ImageField(upload_to='about/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'About Page'
        verbose_name_plural = 'About Page'
    
    def __str__(self):
        return self.title


class Applications(models.Model):
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='applications/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = FroalaField(
        options={
            'toolbarInline': True,
        }
    )
    image = models.ImageField(upload_to='blog/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
    
    def __str__(self):
        return self.title
    