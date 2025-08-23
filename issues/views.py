from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Issue

@login_required
def dashboard(request):
    """Dashboard view - shows overview"""
    user_projects = Project.objects.filter(created_by=request.user)
    user_issues = Issue.objects.filter(created_by=request.user)
    
    context = {
        'projects': user_projects,
        'issues': user_issues,
        'total_projects': user_projects.count(),
        'total_issues': user_issues.count(),
        'open_issues': user_issues.filter(status='Open').count(),
    }
    return render(request, 'issues/dashboard.html', context)

@login_required
def project_list(request):
    """List all projects for current user"""
    projects = Project.objects.filter(created_by=request.user)
    return render(request, 'issues/project_list.html', {'projects': projects})

@login_required
def project_create(request):
    """Create a new project"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        
        if name:
            project = Project.objects.create(
                name=name,
                description=description,
                created_by=request.user
            )
            messages.success(request, f'Project "{project.name}" created successfully!')
            return redirect('project_list')
    
    return render(request, 'issues/project_create.html')

@login_required
def issue_list(request):
    """List all issues for current user"""
    issues = Issue.objects.filter(created_by=request.user)
    return render(request, 'issues/issue_list.html', {'issues': issues})

@login_required
def issue_create(request):
    """Create a new issue"""
    projects = Project.objects.filter(created_by=request.user)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        project_id = request.POST.get('project')
        priority = request.POST.get('priority', 'Medium')
        
        if title and project_id:
            project = get_object_or_404(Project, id=project_id, created_by=request.user)
            
            issue = Issue.objects.create(
                title=title,
                description=description,
                project=project,
                priority=priority,
                created_by=request.user
            )
            messages.success(request, f'Issue "{issue.title}" created successfully!')
            return redirect('issue_list')
    
    return render(request, 'issues/issue_create.html', {'projects': projects})