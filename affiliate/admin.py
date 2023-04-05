from django.contrib import admin
from .models import AffiliateConnection, AffiliateSettled, OrganizationCommision, OrganizationSettled


@admin.register(AffiliateConnection)
class AffiliateConnectionAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'organization', 'commision', 'date', 'isSettled')
    list_filter = ('affiliate', 'organization', 'isSettled')
    search_fields = ('affiliate__user__email', 'organization__name')


@admin.register(AffiliateSettled)
class AffiliateSettledAdmin(admin.ModelAdmin):
    list_display = ('affiliate', 'value', 'date', 'totalConnects')
    list_filter = ('affiliate', 'date')
    search_fields = ('affiliate__user__email',)


@admin.register(OrganizationCommision)
class OrganizationCommisionAdmin(admin.ModelAdmin):
    list_display = ('organization', 'product', 'commision', 'date', 'isSettled')
    list_filter = ('organization', 'product', 'isSettled')
    search_fields = ('organization__name', 'product__name')


@admin.register(OrganizationSettled)
class OrganizationSettledAdmin(admin.ModelAdmin):
    list_display = ('organization', 'value', 'date', 'totalConnects')
    list_filter = ('organization', 'date')
    search_fields = ('organization__name',)
