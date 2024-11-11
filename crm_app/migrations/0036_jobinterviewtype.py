# Generated by Django 5.1.2 on 2024-11-07 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm_app', '0035_merge_20241107_1400'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobInterviewType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobinterviewType', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
            ],
        ),
    ]