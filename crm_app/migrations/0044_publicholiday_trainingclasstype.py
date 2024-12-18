# Generated by Django 5.1.2 on 2024-11-12 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0043_jobinterview'),
    ]

    operations = [
        migrations.CreateModel(
            name='PublicHoliday',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('holiday_name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('from_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='TrainingClassType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tranningTypeId', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
