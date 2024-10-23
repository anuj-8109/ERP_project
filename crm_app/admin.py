from django.contrib import admin

from .models import UserSignup, Profile, RegisterUser, Contacts, Leads, Opportunities, Invoice, Calls, Calendar

# Register your models here.
admin.site.register(UserSignup)


class ContactsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email_id', 'contact_number', 'job_title', 'created_by', 'assigned_to', 'date')
    search_fields = ('first_name', 'last_name', 'email_id', 'contact_number', 'job_title')
    list_filter = ('created_by', 'assigned_to', 'date')

class OpportunitiesAdmin(admin.ModelAdmin):
    list_display = ('opportunity_name', 'amount', 'sale_stage', 'probability', 'expected_close_date', 'lead_source', 'date', 'lead', 'assigned_to')
    search_fields = ('opportunity_name', 'lead__lead_name', 'lead__email_id', 'assigned_to__email')
    list_filter = ('sale_stage', 'assigned_to', 'date')

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'valid_until', 'approval_status', 'opportunity', 'quote_stage', 'invoice_status', 'lead_source', 'account')
    search_fields = ('title', 'opportunity__opportunity_name', 'lead_source__lead_name', 'account')
    list_filter = ('approval_status', 'invoice_status', 'quote_stage', 'valid_until')

class CallsAdmin(admin.ModelAdmin):
    list_display = ('contact', 'call_recording')
    search_fields = ('contact__first_name', 'contact__last_name')
    list_filter = ('contact',)

class CalendarAdmin(admin.ModelAdmin):
    list_display = ('date', 'task', 'time', 'contact', 'meet_links')
    search_fields = ('task', 'contact__first_name', 'contact__last_name')
    list_filter = ('date', 'contact')

admin.site.register(RegisterUser)
admin.site.register(Leads)
admin.site.register(Contacts, ContactsAdmin)
admin.site.register(Opportunities, OpportunitiesAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Calls, CallsAdmin)
admin.site.register(Calendar, CalendarAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone_number', 'date_of_birth')  # Add all fields you want to display
    search_fields = ('user__username', 'first_name', 'last_name')  # Optional: enable search by username or names
    list_filter = ('date_of_birth',)


# admin.site.register(MiningData)

##################################### Budget & Forecasting #####################################################

from .models import Company, Department, DepartmentBudget, BudgetRequest

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'allocated_budget', 'budget_year')
    search_fields = ('name', 'code')
    list_filter = ('budget_year',)
    ordering = ('name',)
    fields = ('name', 'code', 'allocated_budget', 'budget_year')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'company')
    search_fields = ('name',)
    list_filter = ('company',)
    ordering = ('name',)
    fields = ('name', 'company')

@admin.register(DepartmentBudget)
class DepartmentBudgetAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'start_date', 'end_date', 'allocated_amount')
    search_fields = ('department__name',)
    list_filter = ('start_date', 'end_date', 'department__company')
    ordering = ('-start_date',)
    fields = ('department', 'start_date', 'end_date', 'allocated_amount')

class BudgetRequestAdmin(admin.ModelAdmin):
    list_display = (
        'budget_name', 
        'company', 
        'department', 
        'allocated_amount', 
        'start_date', 
        'end_date', 
        'status'
    )
    list_filter = ('company', 'department', 'status', 'start_date', 'end_date')
    search_fields = ('budget_name', 'company__name', 'department__name')
    date_hierarchy = 'start_date'
    readonly_fields = ('status',)
    ordering = ('-start_date',)

admin.site.register(BudgetRequest, BudgetRequestAdmin)