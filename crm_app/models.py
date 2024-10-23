from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, EmailValidator, MinValueValidator, MaxValueValidator
import uuid
from django.core.exceptions import ValidationError

# Model for user signup
class UserSignup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Token for {self.user.email}'

# Model for Register User
class RegisterUser(models.Model):
    email = models.EmailField(max_length=255, unique=True, validators=[EmailValidator(message="Enter a valid email address.")])
    user_role = models.CharField(max_length=255)
    emp_id = models.CharField(max_length=15, unique=True)
    date_of_birth = models.DateField()
    branch = models.CharField(max_length=255)

    def __str__(self):
        return self.email

# Model for Contacts
class Contacts(models.Model):
    phone_number_validator = RegexValidator(regex=r'^\d{10}$', message="Contact number must be exactly 10 digits.")
    email_validator = EmailValidator(message="Enter a valid email address.")

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField(max_length=255, unique=True, validators=[email_validator])
    contact_number = models.CharField(max_length=15, validators=[phone_number_validator])
    job_title = models.CharField(max_length=255)
    created_by = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, related_name='created_contacts')
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, related_name='assigned_contacts')
    date = models.DateField()
    organisation_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email_id})"

    def clean(self):
        if not self.contact_number.isdigit():
            raise ValidationError("Contact number should only contain numbers.")

# Model for Leads
class Leads(models.Model):
    phone_number_validator = RegexValidator(regex=r'^\d{10}$', message="Contact number must be exactly 10 digits.")
    email_validator = EmailValidator(message="Enter a valid email address.")

    lead_name = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_id = models.EmailField(max_length=255, unique=True, validators=[email_validator])
    contact_number = models.CharField(max_length=15, validators=[phone_number_validator])
    address = models.TextField()
    date = models.DateField()
    contact_link = models.CharField(max_length=500)
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    created_by = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, related_name='created_leads')
    remark = models.TextField(blank=True, null=True)
    next_date = models.DateField()
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name='leads')

    def __str__(self):
        return f"{self.lead_name} ({self.first_name} {self.last_name})"

    def clean(self):
        if not self.contact_number.isdigit():
            raise ValidationError("Contact number should only contain numbers.")

# Model for Opportunities
class Opportunities(models.Model):
    opportunity_name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    sale_stage = models.CharField(max_length=255)
    probability = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
    description = models.TextField(blank=True, null=True)
    expected_close_date = models.DateField()
    lead_source = models.CharField(max_length=500)
    date = models.DateField()
    lead = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='opportunities')
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.SET_NULL, null=True, related_name='assigned_opportunities')

    def __str__(self):
        return self.opportunity_name

    def clean(self):
        if self.probability < 0 or self.probability > 100:
            raise ValidationError("Probability must be between 0 and 100.")

# Model for Invoice
class Invoice(models.Model):
    title = models.CharField(max_length=255)
    valid_until = models.DateField()
    approval_status = models.CharField(max_length=50)
    opportunity = models.ForeignKey(Opportunities, on_delete=models.CASCADE, related_name='invoices')
    quote_stage = models.CharField(max_length=50)
    invoice_status = models.CharField(max_length=50)
    approval_issue_description = models.TextField(blank=True, null=True)
    lead_source = models.ForeignKey(Leads, on_delete=models.CASCADE, related_name='invoices')
    account = models.CharField(max_length=255)

    def __str__(self):
        return self.title

# Model for Calls
class Calls(models.Model):
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name='calls')
    call_recording = models.FileField(upload_to='call_recordings/')

    def __str__(self):
        return f"Call with {self.contact.first_name} {self.contact.last_name}"

# Model for Calendar
class Calendar(models.Model):
    date = models.DateField()
    meet_links = models.URLField(max_length=500, blank=True, null=True)
    contact = models.ForeignKey(Contacts, on_delete=models.CASCADE, related_name='calendar_entries')
    task = models.CharField(max_length=255)
    time = models.TimeField()

    def __str__(self):
        return f"{self.task} on {self.date} at {self.time} with {self.contact.first_name}"

# Model for Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

# Validator for phone numbers
phone_number_validator = RegexValidator(
    regex=r'^\+?\d{10,15}$',
    message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
)

# Model for MiningData
class MiningData(models.Model):
    organisation_name = models.CharField(max_length=50, primary_key=True)
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_address = models.TextField()
    customer_contact_number = models.CharField(max_length=15, validators=[phone_number_validator])
    customer_mobile_number = models.CharField(max_length=15, validators=[phone_number_validator])
    customer_email = models.EmailField()
    company_revenue = models.DecimalField(max_digits=12, decimal_places=2)
    company_emp_size = models.IntegerField()
    customer_offering = models.CharField(max_length=30)
    competition_of_AT = models.CharField(max_length=50)
    stock_market_registered = models.CharField(max_length=20)
    influncer = models.BooleanField(default=False)
    decision_maker = models.BooleanField(default=False)
    IT_spending_budget = models.CharField(max_length=30)
    source_of_data_mining = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, null=True, blank=True)
    created_by = models.ForeignKey(RegisterUser, on_delete=models.CASCADE, related_name='mining_data', null=True, blank=True)
    state = models.CharField(max_length=50, default='MP')
    city = models.CharField(max_length=50, default='Indore')
    region = models.CharField(max_length=50, default='North')

    def __str__(self):
        return self.organisation_name

# Model for Overview
class Overview(models.Model):
    title = models.CharField(max_length=100)
    opportunity = models.ForeignKey(Opportunities, on_delete=models.CASCADE, related_name='overviews')
    quote_number = models.CharField(max_length=50)
    quote_stage = models.CharField(max_length=50)
    valid_until = models.DateField()
    invoice_status = models.CharField(max_length=50)
    assigned_to = models.ForeignKey(RegisterUser, on_delete=models.CASCADE)
    payment_terms = models.TextField(null=True, blank=True)
    approval_status = models.CharField(max_length=50)
    approval_issue = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.opportunity}"
    

##################################### Budget & Forecasting #####################################################

class Company(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=10, unique=True)
    allocated_budget = models.DecimalField(max_digits=10, decimal_places=2)
    budget_year = models.IntegerField()

class Department(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class DepartmentBudget(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)

class BudgetRequest(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    budget_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    comment = models.TextField(null=True, blank=True)
    allocated_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='Pending')  # 'Pending', 'Approved'

    def __str__(self):
        return f"{self.budget_name} - {self.status}"