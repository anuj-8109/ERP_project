# Generated by Django 5.1.2 on 2024-10-28 11:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0015_budgetrequest'),
    ]

    operations = [
        migrations.CreateModel(
            name='PayGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grade_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SalaryStepGrade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('step_name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='HR_Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('first_name', models.CharField(max_length=100)),
                ('middle_initial', models.CharField(blank=True, max_length=10, null=True)),
                ('last_name', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=100)),
                ('planned_start_date', models.DateField(blank=True, null=True)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=20)),
                ('phone_code', models.CharField(max_length=10)),
                ('phone_number', models.CharField(max_length=15)),
                ('employee_id', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('internal_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.department')),
            ],
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_date', models.DateField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('comments', models.TextField(blank=True, null=True)),
                ('manual_pay_grade', models.CharField(blank=True, max_length=50, null=True)),
                ('manual_salary_step', models.CharField(blank=True, max_length=50, null=True)),
                ('period_type_id', models.CharField(choices=[('FISCAL_BIWEEK', 'Fiscal Bi-Week'), ('FISCAL_MONTH', 'Fiscal Month'), ('FISCAL_QUARTER', 'Fiscal Quarter'), ('FISCAL_WEEK', 'Fiscal Week'), ('FISCAL_YEAR', 'Fiscal Year'), ('RATE_HOUR', 'Rate amount per Hour'), ('RATE_QUARTER', 'Rate amount per Quarter'), ('RATE_WEEK', 'Rate amount per Week'), ('RATE_MONTH', 'Rate amount per Month'), ('SALES_MONTH', 'Sales Month'), ('SALES_QUARTER', 'Sales Quarter')], max_length=50)),
                ('internal_organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.department')),
                ('employment_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm_app.hr_employee', to_field='employee_id')),
                ('pay_grade_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm_app.paygrade')),
                ('salary_step_sequence_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='crm_app.salarystepgrade')),
            ],
        ),
    ]
