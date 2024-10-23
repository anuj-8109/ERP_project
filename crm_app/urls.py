# CRM_APP/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
from django.contrib.auth import views as authentication_views


urlpatterns = [
    path('', RedirectView.as_view(url='/login/', permanent=False)),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('signup-success/', views.signup_success, name='signup_success'),
    
    path('viewprofile/', views.viewprofile, name='viewprofile'),
    path('profile/', views.profile_view, name='profile'),
    path('edit_profile/', views.edit_profile_view, name='edit_profile'),
    path('PerDeshbord/', views.PerDeshbord, name='PerDeshbord'),
    path('improvement/', views.improvement, name='improvement'),
    path('company/', views.company, name='company'),
    path('Employee/', views.Employee, name='Employee'),
    path('report/', views.report, name='report'),
    path('review/', views.review, name='review'),
    path('viewreport/', views.viewreport, name='viewreport'),
    path('forecasting/', views.forecasting, name='forecasting'),

    
    
    
    
 
    path("password_reset/", authentication_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset_done/", authentication_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>", authentication_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", authentication_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    
################################################## Budgeting & Forecasting #############################################################

    path('overview/', views.overview, name='overview'),

    path('create-company/', views.create_company_view, name='create_company'),
    path('api/create-company/', views.create_company, name='create_company_api'),
    path('api/companies/', views.get_companies, name='get_companies'),
    path('api/company/<int:company_id>/', views.get_company, name='get_company'),

    path('manage-departments/', views.manage_departments_view, name='manage_departments'),
    path('api/departments/<int:company_id>/', views.get_departments, name='get_departments'),
    path('api/add-departments/', views.add_departments, name='add_departments'),
    path('api/add-department-budget/', views.add_department_budget, name='add_department_budget'),

    path('api/submit-budget/', views.submit_budget, name='submit_budget'),
    path('api/department-budgets/<int:company_id>/', views.get_department_budgets, name='get_department_budgets'),

    path('request-budget/', views.requestBudget, name='request_budget'),
    path('create/', views.create_budget_request, name='create_budget_request'),
    path('budget/<int:budget_id>/', views.budget_request_detail, name='budget_request_detail'),
    
    path('budgetReport/', views.report_view, name='budgetReport'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)