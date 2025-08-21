from django.shortcuts import render

# Create your views here.

from .models import *
from django.db.models import Q

def issue_list(request):
    issues = Issue.objects.all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        issues = issues.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filter by status
    status_filter = request.GET.get('status', '')
    if status_filter:
        issues = issues.filter(status=status_filter)
    
    # Filter by priority
    priority_filter = request.GET.get('priority', '')
    if priority_filter:
        issues = issues.filter(priority=priority_filter)
    
    return render(request, 'issues/issue_list.html', {'issues': issues})