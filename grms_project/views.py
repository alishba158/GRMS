from django.shortcuts import render
from django.http import HttpResponse

def home_view(request):
    """Home page view"""
    return render(request, 'home.html')

def team_view(request):
    """Team page view"""
    return render(request, 'team.html')

def about_view(request):
    """About page view"""
    return render(request, 'about.html')

def contact_view(request):
    """Contact page view"""
    return render(request, 'contact.html')