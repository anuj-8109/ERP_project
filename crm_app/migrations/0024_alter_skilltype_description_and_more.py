# Generated by Django 5.1.2 on 2024-11-04 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0023_alter_skilltype_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skilltype',
            name='description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='skilltype',
            name='skillTypeId',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
