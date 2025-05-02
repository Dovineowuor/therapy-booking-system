from django.contrib import admin
from .models import Category, Project, ProjectImage, Testimonial

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

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'company', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'company', 'quote')
