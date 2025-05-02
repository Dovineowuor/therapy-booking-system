from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('', views.portfolio, name='portfolio'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('testimonials/', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('careers/', views.CareerListView.as_view(), name='careers'),
    path('careers/<int:pk>/', views.CareerDetailView.as_view(), name='career_detail'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('careers/', views.career, name='careers'),
    path('careers/<slug:slug>/', views.career_detail, name='career_detail'),
    path('blogs/', views.blog, name='blog'),
    path('blogs/<slug:slug>/', views.blog_detail, name='blog_detail'),
]