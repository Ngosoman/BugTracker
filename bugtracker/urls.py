from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from issues import views  # Import views directly

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    
    # Direct URL mappings
    path('dashboard/', views.dashboard, name='dashboard'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.project_create, name='project_create'),
    path('issues/', views.issue_list, name='issue_list'),
    path('issues/create/', views.issue_create, name='issue_create'),
    
    path('accounts/', include('django.contrib.auth.urls')),
]