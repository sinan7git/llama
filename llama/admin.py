from django.contrib import admin
from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    search_fields = ['name', 'description', 'type', 'supplier_category', 'legal_structure']


admin.site.register(Company, CompanyAdmin)
