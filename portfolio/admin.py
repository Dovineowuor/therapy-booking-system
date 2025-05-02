from django.contrib import admin
from .models import Category, Project, ProjectImage, Testimonial, Career, Applications, About

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 3

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'date_completed', 'is_featured')
    list_filter = ('category', 'is_featured', 'date_completed')
    search_fields = ('title', 'description', 'client')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'date_completed'
    inlines = [ProjectImageInline]

@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'job_type', 'location', 'is_remote', 'salary_range', 'is_active', 'created_at')
    list_filter = ('department', 'job_type', 'location', 'is_remote', 'is_active')
    search_fields = ('title', 'description', 'requirements', 'responsibilities', 'experience_required')
    list_editable = ('is_active',)
    fieldsets = (
        ('Job Details', {
            'fields': ('title', 'department', 'job_type', 'location', 'is_remote', 'salary_range')
        }),
        ('Requirements', {
            'fields': ('experience_required', 'requirements', 'responsibilities')
        }),
        ('Content', {
            'fields': ('description',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )

@admin.register(ProjectImage)
class ProjectImageAdmin(admin.ModelAdmin):
    list_display = ('project', 'caption')
    list_filter = ('project',)
    search_fields = ('caption',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'company', 'quote')
