from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, OrganizationUser, Affiliate, Customer,\
                    customerOtpStack, EmployeeRole, Employee


class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('phoneNumber', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Personal Info', {'fields': ('name', 'email', 'dateOfBirth', 'avatar')}),
        ('Roles', {'fields': ('isAffiliate', 'isCustomer', 'isMarketEmployee',
                              'isOrganizationAdmin', 'isOrganizationStaff')}),
        ('Tours', {'fields': ('isWebTourDone', 'isAppTourDone', 'isSoftwareTourDone')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phoneNumber', 'password1', 'password2'),
        }),
    )
    list_display = ('phoneNumber', 'name', 'email', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'is_superuser', 'isAffiliate', 'isCustomer',
                   'isMarketEmployee', 'isOrganizationAdmin', 'isOrganizationStaff')
    search_fields = ('phoneNumber', 'name', 'email')
    ordering = ('phoneNumber',)


class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'whatsapp')
    list_filter = ('organization',)
    search_fields = ('user__phoneNumber', 'user__name', 'organization__name')


class AffiliateAdmin(admin.ModelAdmin):
    list_display = ('user', 'referCode', 'commissionPercentage', 'revenue')
    search_fields = ('user__phoneNumber', 'user__name', 'referCode')
    list_filter = ('commissionPercentage',)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'isVerified')
    search_fields = ('user__phoneNumber', 'user__name')
    list_filter = ('isVerified',)


class CustomerOtpStackAdmin(admin.ModelAdmin):
    list_display = ('phoneNumber', 'otp', 'dateTime')
    search_fields = ('phoneNumber',)
    list_filter = ('dateTime',)


class EmployeeRoleAdmin(admin.ModelAdmin):
    list_display = ('title',)


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('user', 'address', 'role', 'isManager', 'salary', 'joinedDate', 'phoneNumber')
    search_fields = ('user__phoneNumber', 'user__name', 'address')
    list_filter = ('role', 'isManager', 'joinedDate')



admin.site.register(User, UserAdmin)
admin.site.register(OrganizationUser, OrganizationUserAdmin)
admin.site.register(Affiliate, AffiliateAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(customerOtpStack, CustomerOtpStackAdmin)
admin.site.register(EmployeeRole, EmployeeRoleAdmin)
admin.site.register(Employee, EmployeeAdmin)
