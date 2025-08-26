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
    """View for pasting and analyzing code - FIXED"""
    try:
        if request.method == 'POST':
            title = request.POST.get('title')
            code_content = request.POST.get('code')
            language = request.POST.get('language', 'python')
            
            if title and code_content:
                # Basic analysis
                if language == 'python':
                    issues_found = analyze_python_code_basic(code_content)
                    messages.success(request, f'Found {len(issues_found)} issues in your Python code!')
                    
                    # SHOW RESULTS ON SAME PAGE (instead of redirect)
                    return render(request, 'issues/code_paste.html', {
                        'analysis_results': issues_found,
                        'code_content': code_content,
                        'title': title,
                        'language': language
                    })
                else:
                    messages.info(request, f'Code submitted! {language} analysis coming soon.')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Title and code content are required!')
        
        return render(request, 'issues/code_paste.html')
    
    except Exception as e:
        print(f"ERROR: {str(e)}")
        messages.error(request, f'An error occurred: {str(e)}')
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
    """Enhanced Python code analysis"""
    issues = []
    lines = code.split('\n')
    
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Check for multiple issues per line
        checks = [
            # Python 2 print syntax
            {
                'pattern': r'print\s+[^\(]',
                'type': 'Python 2 Syntax',
                'description': 'print statement without parentheses (Python 2 style)',
                'severity': 'medium',
                'fix': lambda l: re.sub(r'print\s+([^\(].*)', r'print(\1)', l)
            },
            # None comparison
            {
                'pattern': r'==\s*None|\!=\s*None',
                'type': 'None Comparison',
                'description': 'Use "is" or "is not" for None comparisons (PEP 8)',
                'severity': 'low',
                'fix': lambda l: l.replace(' == None', ' is None').replace(' != None', ' is not None')
            },
            # Bare except
            {
                'pattern': r'^\s*except:',
                'type': 'Bare Except Clause',
                'description': 'Bare except clause - specify exception type',
                'severity': 'medium',
                'fix': lambda l: l.replace('except:', 'except Exception:')
            },
            # Old style class
            {
                'pattern': r'^class\s+\w+[^\(]:',
                'type': 'Old-style Class',
                'description': 'Use new-style classes (inherit from object)',
                'severity': 'low',
                'fix': lambda l: l.replace(':', '(object):')
            }
        ]
        
        for check in checks:
            if re.search(check['pattern'], line):
                issues.append({
                    'line_number': i,
                    'issue_type': check['type'],
                    'description': check['description'],
                    'severity': check['severity'],
                    'suggested_fix': check['fix'](line),
                    'original_line': line
                })
                break  
    
    return issues

@login_required
def my_code_list(request):
    """List all code snippets for current user"""
    snippets = CodeSnippet.objects.filter(created_by=request.user).order_by('-created_at')
    return render(request, 'issues/my_code_list.html', {'snippets': snippets})