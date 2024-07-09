from django.contrib import admin
from .models import UserProfile,Team
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = UserProfile
        
class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = UserProfile
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            UserProfile.objects.get(username=username)
        except UserProfile.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])
    
class UserProfileAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('mobile_number', 'avatar','team')}),
    )


# Register your models here.
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Team)