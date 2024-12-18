# Generated by Django 5.1.2 on 2024-11-05 04:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0026_alter_employeeposition_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employeeposition',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='crm_app.hr_employee', to_field='employee_id'),
        ),
    ]
