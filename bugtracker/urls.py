from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from issues import views as issues_views
from accounts import views as accounts_views 
import issues.views as views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),

    path('paste-code/', views.paste_code, name='paste_code'), 
    path('my-code/', views.my_code_list, name='my_code_list'),
    
    

    # Issues URLs
    path('dashboard/', issues_views.dashboard, name='dashboard'),
    path('projects/', issues_views.project_list, name='project_list'),
    path('projects/create/', issues_views.project_create, name='project_create'),
    path('issues/', issues_views.issue_list, name='issue_list'),
    path('issues/create/', issues_views.issue_create, name='issue_create'),
    
    # Authentication URLs
    path('accounts/', include('django.contrib.auth.urls')),
    path('signup/', accounts_views.signup, name='signup'),
]