# Generated by Django 5.1.2 on 2024-11-11 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0040_alter_internaljobposting_applicationdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='internaljobposting',
            name='status',
            field=models.CharField(choices=[('Applied', 'Applied'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Applied', max_length=20),
        ),
    ]
