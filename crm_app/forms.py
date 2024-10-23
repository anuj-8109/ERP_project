# CRM_APP/forms.py
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Department

class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
    )
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password1 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help texts
        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(label="Enter your email address")

class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput, label="New Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm New Password")

    

class CompanyDepartmentFilterForm(forms.Form):
    company = forms.ModelChoiceField(
        queryset=Company.objects.all(),
        label='Select Company',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.none(),  # Empty initially
        label='Select Department',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        # Initialize the form with the request data if present
        super().__init__(*args, **kwargs)

        # Get selected company from the submitted data (if any)
        selected_company = self.data.get('company')

        if selected_company:
            # Filter departments based on the selected company
            self.fields['department'].queryset = Department.objects.filter(
                company_id=selected_company
            )
        else:
            # Optional: If no company selected, keep department list empty or all
            self.fields['department'].queryset = Department.objects.none()

        # Display names instead of object references in dropdowns
        self.fields['company'].label_from_instance = lambda obj: f"{obj.name}"
        self.fields['department'].label_from_instance = lambda obj: f"{obj.name}"

