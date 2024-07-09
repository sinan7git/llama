# Generated by Django 4.2.13 on 2024-07-04 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llama', '0002_companee_company_hrms_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='division',
            field=models.ManyToManyField(to='llama.companydivisions', verbose_name='Our Division'),
        ),
        migrations.AlterField(
            model_name='company',
            name='main_type',
            field=models.ManyToManyField(to='llama.companytypes'),
        ),
    ]
