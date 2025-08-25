from django.urls import path
from . import views

app_name = 'issues'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Code Paste URLs
    path('paste-code/', views.paste_code, name='paste_code'), 
    path('my-code/', views.my_code_list, name='my_code_list'),
    
    
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.issue_create, name='issue_create'),
]