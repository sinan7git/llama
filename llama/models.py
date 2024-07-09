import os
from django.conf import settings
from django.db import models
import pytz
from .helpers import TimeStampedModel
from model_utils import Choices
from django.contrib.auth.models import User
from django.urls import reverse_lazy


class Companee(models.Model):

    """
    Model to manage all the company details
    """
    all_timezones = [ (index, tz.lower(), tz) for index, tz in enumerate(pytz.all_timezones, 1)]
    COMPANY_TIMEZONE_CHOICES = Choices(*all_timezones)
    FILE_AUTHORIZATIONS = Choices(('V', 'detailed', 'Detailed'),
                                  ('F', 'summary', 'Summary'),
                                  ('A', 'pre_approved', 'PreApproved'),)

    name = models.CharField(max_length=50,
                            blank=True)
    code = models.CharField(max_length=50,
                            blank=True)
    logo = models.FileField(upload_to='normal/company/logo/%y/%m/%d/',
                            blank=True,
                            null=True)
    portal_logo = models.FileField(upload_to='normal/company/logo/%y/%m/%d',
                                   blank=True,
                                   null=True)
    establishment_id = models.CharField(max_length=13, 
                                        blank=True,
                                        null=True)
    manager_name = models.CharField(max_length=50,
                            blank=True, verbose_name="Managed By")
    bank_code = models.CharField(max_length=9,
                                 blank=True)
    timezone = models.PositiveIntegerField(choices=COMPANY_TIMEZONE_CHOICES,
                                           null=True,
                                           blank=True)
    abc_id = models.CharField(max_length=100, blank=True, verbose_name="Financial Year")
    debit_account = models.CharField(max_length=12, blank=True)
    paymentset_code = models.CharField(max_length=3, blank=True)
    file_authorization = models.CharField(choices=FILE_AUTHORIZATIONS,
                                          default=FILE_AUTHORIZATIONS.detailed,
                                          max_length=1)
    # Bank payment vouchers are created when salary is posted for companies
    # with the following tag set as True.
    create_bpv = models.BooleanField(default=False,
                                     verbose_name='Enable Salary Transfer')



    def logo_download_url(self):
        """
        Method to call to checke the persmission to 
        get th file download.
        """
        return reverse_lazy('download_company_logo', kwargs={'pk' : self.pk})

    def portal_logo_download_url(self):
        """
        Method to call to checke the persmission to 
        get th file download.
        """
        return reverse_lazy('download_company_portal_log', kwargs={'pk' : self.pk})

    def get_heirarchy_url(self):
        """
        Method to return employees heirarchy url.
        """
        return reverse_lazy('employees_heirarchy', kwargs={'pk' : self.pk})

    def get_absolute_url(self):
        """
        Return company detail page url.
        """
        return reverse_lazy('detail_hrms_company', kwargs={'pk': self.pk})



    def __unicode__(self):
        return self.name

class CompanyTypes(TimeStampedModel):
    """
    Model to keep the info about  RegistrationCategory.
    """
    name = models.CharField(max_length=120)

    class Meta:
        def __str__(self):
            return self.name
        
    def __unicode__(self):
        """
        Returns human readable object name.
        """
        return self.name


class CompanyDivisions(TimeStampedModel):
    """
    Model to keep the info about  RegistrationCategory.
    """
    name = models.CharField(max_length=120)

    class Meta:
        def __str__(self):
           return self.name

    def __unicode__(self):
        """
        Returns human readable object name.
        """
        return self.name

class Company(TimeStampedModel):
    """
    Model that represents a company aka customer.
    This is the core model of CRM hence resides in :mod:`crm.models`. This may
    move into its own app.
    """
    SUPPLIER_CATEGORY_CHOICES = [('Exclusive Distributor', 'Exclusive Distributor'),
                                 ('Stockist', 'Stockist'),
                                 ('Wholesaler', 'Wholesaler'),
                                 ('Original Equipment Manufacturer (OEM)', 'Original Equipment Manufacturer (OEM)'),
                                 ('Trader', 'Trader'),
                                 ('Service Center', 'Service Center'),
                                 ('E-Commerce', 'E-Commerce'),
                            ]
    COMPANY_TYPE_CHOICES = [('Oil Producer', 'Oil Producer'),
                            ('Gas Producer', 'Gas Producer'),
                            ('Contractor', 'Contractor'),
                            ('Consultant', 'Consultant'),
                            ('Project Management',
                                'Project Management'),
                            ('Trader', 'Trader'),
                            ('Service Center', 'Service Center'),
                            ('E-Commerce', 'E-Commerce'),
                            ('Integrator', 'Integrator'),
                            ('Manufacturer', 'Manufacturer'),
                            ('Skid Builder', 'Skid Builder'),
                            ('Drilling Contractor', 'Drilling Contractor'),
                            ('Well Testing Company', 'Well Testing Company'),
                            ('Refinery', 'Refinery'),
                            ('Petrochemical', 'Petrochemical'),
                            ('Government Organisation',
                                'Government Organisation'),
                            ('Shipping', 'Shipping'),
                            ('Chemicals', 'Chemicals'),
                            ('Transportation', 'Transportation'),
                            ('Utilities', 'Utilities'),
                            ('Supplier', 'Supplier'),
                            ('Financial Services', 'Financial Services'),
                            ('Insurance', 'Insurance'),
                            ('Other', 'Other'),
                            ('Facility Management', 'Facility Management'),
                            ('Building Management', 'Building Management'),
                            ('Oil and Gas', 'Oil and Gas'),
                            ('Electrical Traders', 'Electrical Traders'),
                            ('Recruitment/Manpower Supplier', 'Recruitment/Manpower Supplier'),
                            ('Distributor', 'Distributor'),
                            ('Exclusive Distributor', 'Exclusive Distributor'),
                            ('Stockist', 'Stockist'),
                            ('Wholesaler', 'Wholesaler'),
                            ('Original Equipment Manufacturer (OEM)', 'Original Equipment Manufacturer (OEM)'),
                            ('Competitor', 'Competitor'),
                            ('MQB List', 'MQB List'),
                            ('Ship Building and Ship Repairing', 'Ship Building and Ship Repairing'),
                            ('Service Provider', 'Service Provider'),
                            ('Marine Equipment Repairing and Maintenance', 'Marine Equipment Repairing and Maintenance'),
                            ('Heavy Duty Equipment and Machinery Repairing and Maintenance', 'Heavy Duty Equipment and Machinery Repairing and Maintenance'),
                            ('Measuring and Control System Installation', 'Measuring and Control System Installation'),
                            ('Electromechanical Equipment Installation and Maintenance', 'Electromechanical Equipment Installation and Maintenance'),('Subscription', 'Subscription')]
    LEGAL_STRUCTURE_CHOICES = [('LLC', 'LLC'),
                               ('Sole Proprietorship', 'Sole Proprietorship'),
                               ('Partnership', 'Partnership'),
                               ('Free Zone', 'Free Zone'),
                               ('Service Agent', 'Service Agent'),
                               ('Public Company', 'Public Company'),
                               ('Government Organisation',
                                    'Government Organisation'),
                               ('Private Joint Stock', 'Private Joint Stock'),
                               ('Public Joint Stock', 'Public Joint Stock'),
                               ('Corporation', 'Corporation')]
    NO_OF_EMPLOYEES_CHOICES = [('< 25', '< 25'),
                               ('< 100', '< 100'),
                               ('< 500', '< 500'),
                               ('< 1000', '< 1000'),
                               ('< 5000', '< 5000'),
                               ('< 10000', '< 10000'),
                               ('more than 10000', 'more than 10000')]
    REVENUE_CHOICES = [('< 1 Million AED', '< 1 Million AED'),
                       ('< 5 Million AED', '< 5 Million AED'),
                       ('< 10 Million AED', '< 10 Million AED'),
                       ('< 25 Million AED', '< 25 Million AED'),
                       ('< 50 Million AED', '< 50 Million AED'),
                       ('< 100 Million AED', '< 100 Million AED'),
                       ('< 500 Million AED', '< 500 Million AED'),
                       ('> 500 Million AED', '> 500 Million AED')]
    CREDIT_TERM_CHOICES = [('Cash Advance', 'Cash Advance'),
                           ('Cash Before Shipping', 'Cash Before Shipping'),
                           ('Stage Payment', 'Stage Payment'),
                           ('30 Days', '30 Days'),
                           ('60 Days', '60 Days'),
                           ('Other', 'Other')
                           ]
    COMPANY_MANAGED_BY = [ ('Own Employees', 'Own Employees'),
                           ('Complete Outsourced', 'Complete Outsourced'),
                           ('Partially Outsourced', 'Partially Outsourced')
                         ]

    STATUS_CHOICES = Choices(
        (1, 'new', 'New'),
        (2, 'submitted_for_approval', 'Submitted For Approval'),
        (3, 'approved', "Approved"),
        (4, 'revise', "Revised"),
        (5, 'reject', "Rejected"),
    )

    DEFAULT_LOGO = 'normal/company_logos/default.png'
    code = models.SlugField(editable=False, max_length=500)
    name = models.TextField(verbose_name='Company Legal Name')
    description = models.TextField(blank=True)

    division = models.ManyToManyField(CompanyDivisions,verbose_name="Our Division")
    main_type = models.ManyToManyField(CompanyTypes)
    type = models.CharField(max_length=200,
                            choices=COMPANY_TYPE_CHOICES,
                            default=COMPANY_TYPE_CHOICES[0][0], verbose_name="Sub type")
    hrms_company = models.ForeignKey(Companee,
                                     related_name='internal_company_involved', null=True, blank=True,on_delete=models.CASCADE,
                                     verbose_name="Our Company Involved")
    customer_account_manager = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                 null=True,
                                                 blank=True,
                                                 on_delete=models.CASCADE,
                                                 related_name='assigned_customer_account_manager')
    supplier_account_manager = models.ForeignKey(settings.AUTH_USER_MODEL,
                                                 null=True,
                                                 blank=True,
                                                 on_delete=models.CASCADE,
                                                 related_name='assigned_supplier_account_manager')
    supplier_category = models.CharField(max_length=200,
                            choices=SUPPLIER_CATEGORY_CHOICES,
                            verbose_name="Supplier Category", null=True, blank=True)
    supplier_discount_percentage = models.IntegerField(default=0)
    product_types = models.CharField(blank=True, null=True, max_length=250)
    website = models.URLField(blank=True)
    gas_production = models.FloatField(null=True,
                                       blank=True,
                                       verbose_name='Gas Production (billion cubics feet/day)')
    gas_reserves = models.FloatField(null=True,
                                     blank=True,
                                     verbose_name='Gas Reserves (cubic feet)')
    oil_production = models.FloatField(null=True,
                                       blank=True,
                                       verbose_name='Oil Production (barrels a day)')
    oil_reserves = models.FloatField(null=True,
                                     blank=True,
                                     verbose_name='Oil Reserves (barrels)')
    potential_business_details = models.TextField(blank=True, null=True)
    legal_structure = models.CharField(max_length=30,
                                       choices=LEGAL_STRUCTURE_CHOICES,
                                       default=LEGAL_STRUCTURE_CHOICES[0][0])
    no_of_employees = models.CharField(max_length=15,
                                       choices=NO_OF_EMPLOYEES_CHOICES,
                                       default=NO_OF_EMPLOYEES_CHOICES[0][0])
    revenue = models.CharField(max_length=20,
                               choices=REVENUE_CHOICES,
                               default=REVENUE_CHOICES[0][0])
    tax_registration_number = models.CharField(max_length=80, blank=True, null=True)
    custom_category = models.CharField(max_length=250, blank=True, null=True)
    logo = models.ImageField(upload_to='normal/company_logos/%y/%m/%d/',
                             default=DEFAULT_LOGO,
                             blank=True)
    # Following financial fields will be only updated at a later time after
    # approval from financial manager.
    approved_credit_limit = models.DecimalField(max_digits=10,
                                                decimal_places=2,
                                                default=0)
    # default is cash advance
    credit_term = models.CharField(max_length=40,
                                   choices=CREDIT_TERM_CHOICES,
                                   default=CREDIT_TERM_CHOICES[0][0])
    managed_by = models.CharField(max_length=40,
                                   choices=COMPANY_MANAGED_BY,
                                   default=COMPANY_MANAGED_BY[0][0])
    credit_approved_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                           related_name='approved_credits',
                                           null=True,
                                           blank=True,
                                           on_delete=models.CASCADE)
    # Some companies have approvals inherited from other giant companies.
    # So we reference these like company.approval_parent.approvals
    approval_parent = models.ForeignKey('self',
                                        related_name='approval_dependencies',
                                        null=True,
                                        blank=True,
                                        on_delete=models.CASCADE,
                                        verbose_name='Inherit approvals from')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   related_name='created_companies',
                                   editable=False,
                                   null=True,
                                   on_delete=models.CASCADE,
                                   blank=True)
    modified_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='modified_companies',
                                    editable=False,
                                    null=True,
                                    on_delete=models.CASCADE,
                                    blank=True)
    # Following two fields are only applicable if the company type 
    # is shipping
    approved_forwarding_agent = models.BooleanField(default=False)
    rating = models.IntegerField(default=50)
    status = models.PositiveIntegerField(choices=STATUS_CHOICES,
                                         blank=False,
                                         default=STATUS_CHOICES.new)

    class Meta:
        permissions = (
                    ('access_all_companies', 'Permission to view all companies'),)
        
    def __str__(self):
        return self.name

    def country(self):
        """
        Find the country from the addresses. If there are no addresses return
        nothing.
        """
        if self.addresses.all():
            return self.addresses.all()[0].country

    def get_logo_url(self):
        """
        Returns the url to access the logo, if no image is a present url of
        default image will be given. The reason for adding this method is a bug
        when user delete the logo of the company on editing a company.

        :returns: str - Path to the logo that can be directly used in template.

        .. note::

            This method should be used in template to show company logo.
        """
        if self.logo:
            return self.logo.url
        else:
            return os.path.join(settings.MEDIA_URL, self.DEFAULT_LOGO)

    def get_absolute_url(self):
        """
        Return the company page detail url.
        Use this like this: company_obj.get_absolute_url()

        :returns: str - Url to the detail page of company
        """
        return reverse_lazy('add_company_detail', kwargs={'pk': self.pk})
        """
        This method populates the code field from the company name before
        saving using :func:`helpers.methods.unique_slugify` 
        """
        # To make the proxy model use the same model character, which cannot be
        # directly mentioned in the setting dict for keeping them as there will
        # be repeatition 
        prepend_character = kwargs.pop('prepend_character', None)
        if not prepend_character:
            prepend_character = get_key_from_dict(settings.MODEL_CODE_CHARACTERS,
                                                  str(self._meta))
        # Set the `code` field an unique slug value generated from `name`
        unique_slugify(self,
                       self.name,
                       prepend_character=prepend_character)
        super(Company, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name