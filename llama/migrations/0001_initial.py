# Generated by Django 4.2.13 on 2024-07-04 06:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyDivisions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CompanyTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=120)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('code', models.SlugField(editable=False, max_length=500)),
                ('name', models.TextField(verbose_name='Company Legal Name')),
                ('description', models.TextField(blank=True)),
                ('type', models.CharField(choices=[('Oil Producer', 'Oil Producer'), ('Gas Producer', 'Gas Producer'), ('Contractor', 'Contractor'), ('Consultant', 'Consultant'), ('Project Management', 'Project Management'), ('Trader', 'Trader'), ('Service Center', 'Service Center'), ('E-Commerce', 'E-Commerce'), ('Integrator', 'Integrator'), ('Manufacturer', 'Manufacturer'), ('Skid Builder', 'Skid Builder'), ('Drilling Contractor', 'Drilling Contractor'), ('Well Testing Company', 'Well Testing Company'), ('Refinery', 'Refinery'), ('Petrochemical', 'Petrochemical'), ('Government Organisation', 'Government Organisation'), ('Shipping', 'Shipping'), ('Chemicals', 'Chemicals'), ('Transportation', 'Transportation'), ('Utilities', 'Utilities'), ('Supplier', 'Supplier'), ('Financial Services', 'Financial Services'), ('Insurance', 'Insurance'), ('Other', 'Other'), ('Facility Management', 'Facility Management'), ('Building Management', 'Building Management'), ('Oil and Gas', 'Oil and Gas'), ('Electrical Traders', 'Electrical Traders'), ('Recruitment/Manpower Supplier', 'Recruitment/Manpower Supplier'), ('Distributor', 'Distributor'), ('Exclusive Distributor', 'Exclusive Distributor'), ('Stockist', 'Stockist'), ('Wholesaler', 'Wholesaler'), ('Original Equipment Manufacturer (OEM)', 'Original Equipment Manufacturer (OEM)'), ('Competitor', 'Competitor'), ('MQB List', 'MQB List'), ('Ship Building and Ship Repairing', 'Ship Building and Ship Repairing'), ('Service Provider', 'Service Provider'), ('Marine Equipment Repairing and Maintenance', 'Marine Equipment Repairing and Maintenance'), ('Heavy Duty Equipment and Machinery Repairing and Maintenance', 'Heavy Duty Equipment and Machinery Repairing and Maintenance'), ('Measuring and Control System Installation', 'Measuring and Control System Installation'), ('Electromechanical Equipment Installation and Maintenance', 'Electromechanical Equipment Installation and Maintenance'), ('Subscription', 'Subscription')], default='Oil Producer', max_length=200, verbose_name='Sub type')),
                ('supplier_category', models.CharField(blank=True, choices=[('Exclusive Distributor', 'Exclusive Distributor'), ('Stockist', 'Stockist'), ('Wholesaler', 'Wholesaler'), ('Original Equipment Manufacturer (OEM)', 'Original Equipment Manufacturer (OEM)'), ('Trader', 'Trader'), ('Service Center', 'Service Center'), ('E-Commerce', 'E-Commerce')], max_length=200, null=True, verbose_name='Supplier Category')),
                ('supplier_discount_percentage', models.IntegerField(default=0)),
                ('product_types', models.CharField(blank=True, max_length=250, null=True)),
                ('website', models.URLField(blank=True)),
                ('gas_production', models.FloatField(blank=True, null=True, verbose_name='Gas Production (billion cubics feet/day)')),
                ('gas_reserves', models.FloatField(blank=True, null=True, verbose_name='Gas Reserves (cubic feet)')),
                ('oil_production', models.FloatField(blank=True, null=True, verbose_name='Oil Production (barrels a day)')),
                ('oil_reserves', models.FloatField(blank=True, null=True, verbose_name='Oil Reserves (barrels)')),
                ('potential_business_details', models.TextField(blank=True, null=True)),
                ('legal_structure', models.CharField(choices=[('LLC', 'LLC'), ('Sole Proprietorship', 'Sole Proprietorship'), ('Partnership', 'Partnership'), ('Free Zone', 'Free Zone'), ('Service Agent', 'Service Agent'), ('Public Company', 'Public Company'), ('Government Organisation', 'Government Organisation'), ('Private Joint Stock', 'Private Joint Stock'), ('Public Joint Stock', 'Public Joint Stock'), ('Corporation', 'Corporation')], default='LLC', max_length=30)),
                ('no_of_employees', models.CharField(choices=[('< 25', '< 25'), ('< 100', '< 100'), ('< 500', '< 500'), ('< 1000', '< 1000'), ('< 5000', '< 5000'), ('< 10000', '< 10000'), ('more than 10000', 'more than 10000')], default='< 25', max_length=15)),
                ('revenue', models.CharField(choices=[('< 1 Million AED', '< 1 Million AED'), ('< 5 Million AED', '< 5 Million AED'), ('< 10 Million AED', '< 10 Million AED'), ('< 25 Million AED', '< 25 Million AED'), ('< 50 Million AED', '< 50 Million AED'), ('< 100 Million AED', '< 100 Million AED'), ('< 500 Million AED', '< 500 Million AED'), ('> 500 Million AED', '> 500 Million AED')], default='< 1 Million AED', max_length=20)),
                ('tax_registration_number', models.CharField(blank=True, max_length=80, null=True)),
                ('custom_category', models.CharField(blank=True, max_length=250, null=True)),
                ('logo', models.ImageField(blank=True, default='normal/company_logos/default.png', upload_to='normal/company_logos/%y/%m/%d/')),
                ('approved_credit_limit', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('credit_term', models.CharField(choices=[('Cash Advance', 'Cash Advance'), ('Cash Before Shipping', 'Cash Before Shipping'), ('Stage Payment', 'Stage Payment'), ('30 Days', '30 Days'), ('60 Days', '60 Days'), ('Other', 'Other')], default='Cash Advance', max_length=40)),
                ('managed_by', models.CharField(choices=[('Own Employees', 'Own Employees'), ('Complete Outsourced', 'Complete Outsourced'), ('Partially Outsourced', 'Partially Outsourced')], default='Own Employees', max_length=40)),
                ('approved_forwarding_agent', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=50)),
                ('status', models.PositiveIntegerField(choices=[(1, 'New'), (2, 'Submitted For Approval'), (3, 'Approved'), (4, 'Revised'), (5, 'Rejected')], default=1)),
                ('approval_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approval_dependencies', to='llama.company', verbose_name='Inherit approvals from')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_companies', to=settings.AUTH_USER_MODEL)),
                ('credit_approved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_credits', to=settings.AUTH_USER_MODEL)),
                ('customer_account_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_customer_account_manager', to=settings.AUTH_USER_MODEL)),
                ('division', models.ManyToManyField(blank=True, null=True, to='llama.companydivisions', verbose_name='Our Division')),
                ('main_type', models.ManyToManyField(blank=True, null=True, to='llama.companytypes')),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='modified_companies', to=settings.AUTH_USER_MODEL)),
                ('supplier_account_manager', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned_supplier_account_manager', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('access_all_companies', 'Permission to view all companies'),),
            },
        ),
    ]
