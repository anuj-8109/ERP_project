# CRM_APP/views.py
import uuid
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .forms import SignupForm, LoginForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from .models import UserSignup, Profile
from .forms import PasswordResetForm, SetNewPasswordForm

from django.contrib import messages
from django.shortcuts import render, redirect

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)  # Create form instance with POST data
        if form.is_valid():  # Check if the form is valid
            user = form.save()  # Save the user to the database
            UserSignup.objects.create(user=user)  # Create a token for the user
            Profile.objects.create(user=user)
            success_message = "Successfully signed up! Please log in."
            return render(request, 'signup.html', {'form': SignupForm(), 'success_message': success_message})  # Show success message

        else:
            error_messages = form.errors.as_data()  # Get error messages
            return render(request, 'signup.html', {'form': form, 'error_messages': error_messages})  # Show error messages

    form = SignupForm()  # Create an empty form instance for GET request
    return render(request, 'signup.html', {'form': form})  # Render the signup page

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                # Retrieve the user based on the provided email
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                messages.error(request, 'Invalid email')
                return redirect('login')

            # Authenticate using the retrieved user object
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid email or password')
                return redirect('login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    from_email = 'aapaitest@gmail.com'


@login_required
def dashboard_view(request):
    profile = None
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
        except Profile.DoesNotExist:
            profile = None  # Handle the case where no profile exists
    
    return render(request, 'dashboard.html', {'profile': profile})

def signup_success(request):
    return render(request, 'signup_success.html')

@login_required
def profile_view(request):
    try:
        profile = Profile.objects.get(user=request.user)  # Fetch the profile
    except Profile.DoesNotExist:
        return redirect('signup')  # Redirect to signup or create a profile

    return render(request, 'profile.html', {'profile': profile})

@login_required
def edit_profile_view(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        profile.first_name = request.POST.get('first_name')
        profile.last_name = request.POST.get('last_name')
        profile.bio = request.POST.get('bio')
        profile.phone_number = request.POST.get('phone_number')
        profile.date_of_birth = request.POST.get('date_of_birth')  # Handle date of birth
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        return redirect('profile')  # Redirect to the profile view after saving

    return render(request, 'edit_profile.html', {'profile': profile})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

def profiles(request):
    return render(request, 'profile.html')

def viewprofile(request):
    return render(request, 'viewprofile.html')

def profileicon(request):
    return render(request, 'profileicon.html')

def PerDeshbord(request):
    return render(request, 'Performance/PerDeshbord.html')

def improvement(request):
    return render(request, 'Performance/improvement.html')

def company(request):
    return render(request, 'Performance/company.html')

def Employee(request):
    return render(request, 'Performance/Employee.html')

def report(request):
    return render(request, 'Performance/report.html')

def review(request):
    return render(request, 'Performance/review.html')

def viewreport(request):
    return render(request, 'Performance/viewreport.html')

##################################### Budget & Forecasting #####################################################

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Company, Department, DepartmentBudget, BudgetRequest
import json
from .forms import CompanyDepartmentFilterForm
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist



def overview(request):
    return render(request, 'budget/overview.html')

def create_company_view(request):
    return render(request, 'budget/create_company.html')

def manage_departments_view(request):
    return render(request, 'budget/manage_departments.html')

@csrf_exempt
def create_company(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        company = Company.objects.create(
            name=data['name'],
            code=data['code'],
            allocated_budget=data['allocated_budget'],
            budget_year=data['budget_year']
        )
        return JsonResponse({'id': company.id, 'name': company.name}, status=201)
    
def get_companies(request):
    companies = Company.objects.values('id', 'name', 'allocated_budget', 'budget_year')
    return JsonResponse(list(companies), safe=False)

def get_company(request, company_id=None):
    if company_id:
        try:
            company = Company.objects.get(id=company_id)
            data = {
                "id": company.id,
                "name": company.name,
                "code": company.code,
                "allocated_budget": str(company.allocated_budget),  # Convert Decimal to String for JSON response
                "budget_year": company.budget_year,
            }
            return JsonResponse(data, status=200)
        except Company.DoesNotExist:
            return JsonResponse({"error": "Company not found"}, status=404)
    else:
        companies = Company.objects.all()
        # Handle the case for returning all companies if necessary

def get_departments(request, company_id):
    # Fetch departments based on the company ID
    departments = Department.objects.filter(company_id=company_id).values_list('name', flat=True)
    return JsonResponse(list(departments), safe=False)

@csrf_exempt
def add_departments(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        try:
            company = Company.objects.get(id=data['company_id'])
        except Company.DoesNotExist:
            return JsonResponse({'error': 'Company not found'}, status=404)

        departments = data['departments']  # Received as an array

        # Clear existing departments to prevent duplicates
        Department.objects.filter(company=company).delete()

        # Add new departments
        for dept_name in departments:
            if dept_name.strip():  # Avoid empty names
                Department.objects.create(company=company, name=dept_name.strip())

        return JsonResponse({'status': 'success'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def add_department_budget(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        department = Department.objects.get(id=data['department_id'])
        DepartmentBudget.objects.create(
            department=department,
            start_date=data['start_date'],
            end_date=data['end_date'],
            allocated_amount=data['allocated_amount']
        )
        return JsonResponse({'status': 'success'}, status=201)
    
def get_department_budgets(request, company_id):
    # Fetch departments related to the specified company
    departments = Department.objects.filter(company_id=company_id)
    
    # Create a list to store department budget details
    budget_details = []
    for department in departments:
        # Fetch the latest budget details for each department
        budgets = DepartmentBudget.objects.filter(department=department)
        for budget in budgets:
            budget_details.append({
                'department': department.name,
                'start_date': budget.start_date,
                'end_date': budget.end_date,
                'allocated_amount': str(budget.allocated_amount),
            })
    
    return JsonResponse(budget_details, safe=False)

@csrf_exempt
def submit_budget(request):
    if request.method == 'POST':
        # Parse JSON data from the request body
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON.'}, status=400)

        company_id = data.get('company_id')  # Add company_id to your data
        department_name = data.get('department')
        budget_amount = data.get('amount')
        start_date = data.get('startDate')
        end_date = data.get('endDate')

        # Ensure all necessary fields are provided
        if not company_id or not department_name or not budget_amount or not start_date or not end_date:
            return JsonResponse({'error': 'All fields are required.'}, status=400)

        try:
            # Fetch the department based on both company_id and department_name
            department = get_object_or_404(Department, name=department_name, company_id=company_id)

            # Clear existing budgets for this department and company
            DepartmentBudget.objects.filter(department=department).delete()

            # Create and save the new budget record
            department_budget = DepartmentBudget(
                department=department,
                start_date=start_date,
                end_date=end_date,
                allocated_amount=budget_amount
            )
            department_budget.save()

            return JsonResponse({'message': 'Budget saved successfully!'}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


def requestBudget(request):
    return render(request, 'budget/request_budget.html')


@csrf_exempt
def create_budget_request(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Retrieve related company and department instances
        company = Company.objects.get(id=data['company'])
        department = Department.objects.get(name=data['department'], company=company)

        # Create and save the budget request
        budget_request = BudgetRequest.objects.create(
            company=company,
            department=department,
            budget_name=data['budget_name'],
            start_date=data['start_date'],
            end_date=data['end_date'],
            comment=data.get('comment', ''),
            allocated_amount=data['allocated_amount'],
        )

        # Send approval email (optional)
        send_mail(
            subject="Budget Approval Request",
            message=f"Click the link to approve the budget: "
                    f"http://127.0.0.1:8000/budget/{budget_request.id}/",
            from_email='aapaitest@gmail.com',
            recipient_list=['singarapunagarjuna18@gmail.com'],
        )

        return JsonResponse({"message": "Budget request submitted successfully."})
    
    return JsonResponse({"error": "Invalid request method."}, status=400)


def budget_request_detail(request, budget_id):
    try:
        # Fetch the budget request based on the ID
        budget_request = BudgetRequest.objects.get(id=budget_id)

        if request.method == 'POST':
            # Update status based on the button clicked
            if 'approve' in request.POST:
                budget_request.status = 'Approved'
            elif 'reject' in request.POST:
                budget_request.status = 'Rejected'
            
            budget_request.save()
            return HttpResponse(f"Budget request {budget_request.status} successfully.")

        # Render the details of the budget request with action buttons
        return render(request, 'budget/budget_request_detail.html', {'budget_request': budget_request})

    except ObjectDoesNotExist:
        return HttpResponse("Budget request not found.", status=404)
    

def report_view(request):
    form = CompanyDepartmentFilterForm(request.GET or None)
    companies = Company.objects.all()
    department_budgets = None
    budget_requests = None  # Holds BudgetRequest data
    data = []  # Default data

    if form.is_valid():
        company = form.cleaned_data.get('company')
        department = form.cleaned_data.get('department')

        if company and not department:
            # Show department budgets for the selected company
            department_budgets = DepartmentBudget.objects.filter(department__company=company)
        elif company and department:
            # Show budget requests for the selected department under the given company
            budget_requests = BudgetRequest.objects.filter(company=company, department=department)
        else:
            # Default: Display all companies with their departments
            data = [
                {
                    'Company': company.name,
                    'Code': company.code,
                    'Allocated_Budget': company.allocated_budget,
                    'Budget_Year': company.budget_year,
                    'Departments': ", ".join(company.department_set.values_list('name', flat=True))
                } for company in companies
            ]

    # Handle export logic if required
    if 'export' in request.GET:
        return export_data_to_excel(data, department_budgets or budget_requests)
    if 'export_pdf' in request.GET:
        return export_data_to_pdf(data)

    return render(request, 'budget/budgetReport.html', {
        'form': form,
        'data': data,
        'department_budgets': department_budgets,
        'budget_requests': budget_requests
    })


def export_data_to_excel(data, department_budgets):
    if department_budgets:
        export_data = [
            {
                'Company': db.department.company.name,
                'Department': db.department.name,
                'Start Date': db.start_date,
                'End Date': db.end_date,
                'Allocated Amount': db.allocated_amount
            } for db in department_budgets
        ]
    else:
        export_data = data

    df = pd.DataFrame(export_data)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="report.xlsx"'
    df.to_excel(response, index=False)
    return response


def export_data_to_pdf(data):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="report.pdf"'

    # Create a canvas object and write data into the PDF
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    # Header
    p.setFont("Helvetica-Bold", 16)
    p.drawString(100, height - 50, "Department Budget Report")

    # Table-like content
    p.setFont("Helvetica", 12)
    y = height - 100  # Start writing below the header

    for row in data:
        p.drawString(50, y, f"Company: {row['Company']}")
        p.drawString(250, y, f"Department: {row['Departments']}")
        p.drawString(450, y, f"Allocated Budget: {row['Allocated_Budget']}")
        y -= 20  # Move down for the next row

        if y < 50:  # If near the bottom, create a new page
            p.showPage()
            y = height - 50

    p.save()  # Save the PDF

    return response
    
def forecasting(request):
    return render(request, 'forecasting/forecasting.html')

