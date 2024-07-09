from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse_lazy
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from django.core.validators import RegexValidator


class Team(models.Model):
    """
    Model to manage many divisions for single department.
    """
    name = models.CharField(max_length=255, blank=True)
    in_charge = models.ForeignKey(settings.AUTH_USER_MODEL,
                                  related_name='team_in_charge',
                                  null=True,
                                  on_delete=models.CASCADE,
                                  blank=True)
    super_visor = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='team_super_visor',
                                    null=True,
                                     on_delete=models.CASCADE,
                                    blank=True)
    hod = models.ForeignKey(settings.AUTH_USER_MODEL,
                            related_name='teams_hod',
                            null=True,
                             on_delete=models.CASCADE,
                            blank=True)

    def __unicode__(self):
        return u"%s" % (self.name)


# Create your models here.
class UserProfile(AbstractUser):
    """
    Way in django 1.5 to add more fields to the User model shipped with it.
    """
    code = models.CharField(max_length=50, editable=False)
    avatar = models.ImageField(upload_to='normal/avatars/%y/%m/%d/',
                               default='normal/avatars/default.png')
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(100, 100)],
                                      format='JPEG',
                                      options={'quality': 60})
    mobile_number = models.CharField(max_length=20,
                                     blank=True,
                                     validators=[
                                         RegexValidator(
                                                regex=r'^\D?(\d{0,3}?)\D{0,2}(\d{3})?\D{0,2}(\d{3})\D?(\d{4})$',
                                                message='Enter valid phone number'
                                                    )])
    password_changed_by = models.ForeignKey('self',
                                            related_name="password_changed_users",
                                            null=True,
                                            on_delete=models.CASCADE,
                                            blank=True)
    password_changed_on = models.DateTimeField(null=True, blank=True)
    team = models.ForeignKey(Team,
                             related_name="teams",
                             on_delete=models.SET_NULL,
                             null=True,
                             blank=True,
                             verbose_name="Section")
    
    class Meta:
        permissions = (
                    ('access_crm', 'Permission to view crm module'),
                    ('access_hrms', 'Permission to view hrms module'),
                    ('access_pdm', 'Permission to view pdm module'),
                    ('access_mes', 'Permission to view mes module'),
                    ('access_reports', 'Permission to view reports module'),
                    ('access_erp', 'Permission to view erp module'),
                    ('access_qaqc', 'Permission to view qaqc module'),
                    ('access_employee_cost',
                     'Permission to view Employee Cost Module'),
                    ('access_opportunities',
                     'Permission to view Opportunities'),
                    ('access_overtime_supervisor', 
                     'Permission to view Overtime for Supervisors Only'),
                    ('access_job_planning', 
                     'Permission to view Job Planning'),
                    ('access_cr', 
                     'Permission to view CR Module'),
                    ('access_job', 
                     'Permission to view Job Module'),
                    ('access_ncr',
                        "Permission to view ncr module"),
                    ('access_near_miss_report',
                        "permissions to view near miss reports"),
                    ('access_incident_report',
                        "permissions to view incident reports"),
                    ('can_access_contact',
                     "permissions to view contacts"),
                    ('can_access_crm_company', 'Can view crm company'),
                    ('access_hod_portal', 'Can access HOD portal'),
                    ('access_hcap_payroll', 'Can access HCAP payroll'),
                    ('access_hcap_documents', 'Can access HCAP documents'),
                    ('access_view_salary', 'Can View Salary'),
                    ('access_company_policy', 'Can View Company Policy'),
                    ('access_hcap_accounts', 'Permission to view HCAP Accounts'),
                    ('access_supplier_evaluation',
                     'Permission to view Supplier Evaluation Module'),
                    ('access_agency_evaluation',
                     'Permission to view Agency Evaluation Module'),
                    ('access_supplier_opportunities',
                     'Permission to view Supplier Opportunities'),
                    ('full_access_to_view_sales_order',
                     'Permission to view Sales Order with Full access'),
                    ('can_access_projects',
                     "permissions to view projects"),
                    ('can_access_office_directory',
                     "permissions to view office directory"),
                    ('can_access_marketing',
                     "permissions to view marketing"),
                    ('all_approvals',
                     "permissions to view all approvals"),
                    ('can_access_workforce_planning',
                     "permissions to view workforce planning"),
                    ('access_recruitment',
                     "permissions to view Recruitment"),
                    ('add_only_crm_users',
                     "permissions to add only CRM users"),
                    ('view_management_goals',
                     "permissions to view management goals"),
                    ('pr_sent_for_approve',
                     'Permission to send manual purchase for review'),
                    ('view_all_opportunities',
                     'Permission to View All Opportunities'),
                    ('view_all_requesition',
                     'Permission to View All Requisition'),
                    ('approve_work_order', 'Can Approve Work Orders'),
                    ('revise_work_order', 'Can Revise Work Orders'),
                    ('view_pending_work_order', 'Can View Pending Work Order'),
                    ('send_work_order_for_approval', 'Can Send Work Order for Approval'),
                    ('can_view_generic_quotes',
                     "permissions to view Quotes module"),
                    ('can_view_margin_calculations',
                     "Permissions to view Margin Calculation"),
                    ('can_view_invoice_status_report',
                     "Permissions to view Invoice Status Report"),
                    ('access_complaint_portal', 'Can access complaint portal'),
                    ('view_open_opportunities',
                     'Permission to View All Open Opportunities'),
                    ('view_all_teams',
                     'Permission to View All Teams Activities'),
                )

    def employee_name(self):
        """
        Return combined firstname and lastname, otherwise return username.
        This can be used in template so that a real name will be shown if first
        name and last name is filled, otherwise username will be shown.
        """
        try:
            if self.employee:
                return "%s %s" % (self.employee.first_name, self.employee.last_name)
            else:
                return self.username
        except Exception as e:
            return self.username
                              
    def full_name(self):
        """
        Return combined firstname and lastname, otherwise return username.
        This can be used in template so that a real name will be shown if first
        name and last name is filled, otherwise username will be shown.
        """
        try:
            if self.employee:
                return "%s %s (%s)" % (self.employee.first_name, self.employee.last_name,self.username)
                # return "%s(%s)" % (self.employee.first_name, self.username)
            else:
                return self.username
        except Exception as e:
            return self.username

    def get_absolute_url(self):
        """
        Return the url to the profile page.
        """
        return reverse_lazy('user_profile', kwargs={'pk': self.pk})


    def __unicode__(self):
        """
        Show the object in a readable way.
        """
        return self.full_name()

