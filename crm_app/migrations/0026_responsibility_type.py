# Generated by Django 5.1.2 on 2024-11-06 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0025_alter_skilltype_skilltypeid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Responsibility_Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('responsibilityTypeId', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('description', models.CharField(max_length=255)),
            ],
        ),
    ]
