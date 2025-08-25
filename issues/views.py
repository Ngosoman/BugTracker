from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Project, Issue
# from .utils import analyze_python_code
from .models import CodeSnippet, CodeIssue
from .utils import analyze_code


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
        else:
            messages.error(request, 'Project name is required!')
    
    return render(request, 'issues/project_create.html')

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
            try:
                project = Project.objects.get(id=project_id, created_by=request.user)
                
                issue = Issue.objects.create(
                    title=title,
                    description=description,
                    project=project,
                    priority=priority,
                    created_by=request.user
                )
                messages.success(request, f'Issue "{issue.title}" created successfully!')
                return redirect('issue_list')
                
            except Project.DoesNotExist:
                messages.error(request, 'Invalid project selected!')
        else:
            messages.error(request, 'Title and project are required!')
    
    return render(request, 'issues/issue_create.html', {'projects': projects})




@login_required
def paste_code(request):
    """View for pasting and analyzing code"""
    if request.method == 'POST':
        title = request.POST.get('title')
        code_content = request.POST.get('code')
        language = request.POST.get('language', 'python')
        description = request.POST.get('description', '')
        use_ai = request.POST.get('use_ai', False)  
        
        if title and code_content:
            # Save code snippet
            snippet = CodeSnippet.objects.create(
                title=title,
                code=code_content,
                language=language,
                description=description,
                created_by=request.user
            )
            
            # Analyze the code
            if language == 'python':
                # Use basic analysis for now (set use_ai=False for basic)
                analysis_result = analyze_code(code_content, language, use_ai=False)
                
                if 'error' in analysis_result:
                    messages.error(request, analysis_result['error'])
                else:
                    # For basic analysis, we get a list of issues
                    issues_found = analysis_result
                    
                    # Save issues to database
                    for issue_data in issues_found:
                        CodeIssue.objects.create(
                            snippet=snippet,
                            line_number=issue_data['line_number'],
                            issue_type=issue_data['issue_type'],
                            description=issue_data['description'],
                            severity=issue_data['severity'],
                            suggested_fix=issue_data.get('suggested_fix', '')
                        )
                    
                    messages.success(request, f'Found {len(issues_found)} issues in your code!')
                    return redirect('code_results', snippet_id=snippet.id)
            
            else:
                messages.info(request, f'Code saved. {language} analysis coming soon!')
                return redirect('dashboard')
                
        else:
            messages.error(request, 'Title and code content are required!')
    
    return render(request, 'issues/code_paste.html')

@login_required
def code_results(request, snippet_id):
    """Show analysis results for a code snippet"""
    snippet = get_object_or_404(CodeSnippet, id=snippet_id, created_by=request.user)
    issues = CodeIssue.objects.filter(snippet=snippet)
    
    return render(request, 'issues/code_results.html', {
        'snippet': snippet,
        'issues': issues,
        'issues_count': issues.count()
    })


import re

def analyze_code(code, language='python'):
    """Basic code analysis function"""
    if language == 'python':
        return analyze_python_code_basic(code)
    return []

def analyze_python_code_basic(code):
    """Basic Python analysis"""
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        if 'print ' in line:
            issues.append({
                'line_number': i,
                'issue_type': 'Python 2 Syntax',
                'description': 'print without parentheses',
                'severity': 'medium',
                'suggested_fix': f'Change to: print({line.split("print ")[1]})'
            })
            
        if ' == None' in line or ' != None' in line:
            issues.append({
                'line_number': i,
                'issue_type': 'None Comparison',
                'description': 'Use "is" instead of "==" for None',
                'severity': 'low',
                'suggested_fix': line.replace(' == None', ' is None').replace(' != None', ' is not None')
            })
    
    return issues

@login_required
def my_code_list(request):
    """List all code snippets for current user"""
    snippets = CodeSnippet.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'issues/my_code_list.html', {'snippets': snippets})  
        