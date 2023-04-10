
from django.contrib import admin
from .models import (
FeatureCategory,
Feature,
Plan,
CustomPlan,
OrganizationCategory,
OrganizationEventCategory,
OrganizationTier,
Organization,
)
from .models import OrganizationWebpageTemplate, OrganizationWebpage, OrganizationEcardTemplate, OrganizationEcard,OrganizationSchedule


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'htmlId']

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(CustomPlan)
class CustomPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']

@admin.register(OrganizationCategory)
class OrganizationCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'isFaceRecognitionEnable', 'isProductionToolsEnable']

@admin.register(OrganizationEventCategory)
class OrganizationEventCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'thumbnail', 'description', 'isFaceRecognitionEnable']

@admin.register(OrganizationTier)
class OrganizationTierAdmin(admin.ModelAdmin):
    list_display = ['title', 'avgQuotation']

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    icon_name ='business'
    name ='Organization (photo studios)'
    list_display = ['name', 'category', 'tier', 'proprietor', 'status', 'lastUpdated']
    search_fields = ['name', 'proprietor__username']
    list_filter = ['category', 'tier', 'status']








class OrganizationWebpageTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'templateName', 'uploadedAt')
    search_fields = ('templateName', 'uploadedAt')


class OrganizationWebpageAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'isActive', 'isPublic', 'passCode', 'organization', 'template')
    search_fields = ('uuid', 'passCode', 'organization__name')
    list_filter = ('isActive', 'isPublic', 'organization', 'template')


class OrganizationEcardTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'templateName', 'uploadedAt')
    search_fields = ('templateName', 'uploadedAt')


class OrganizationEcardAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'isActive', 'passCode', 'organization', 'template')
    search_fields = ('uuid', 'passCode', 'organization__name')
    list_filter = ('isActive', 'organization', 'template')


class OrganizationScheduleAdmin(admin.ModelAdmin):
    list_display = ('id', 'organization', 'title', 'createdAt', 'scheduledAt', 'status')
    list_filter = ('organization', 'createdAt', 'scheduledAt', 'status')
    search_fields = ('title', 'description')
    ordering = ('-scheduledAt',)

admin.site.register(OrganizationSchedule, OrganizationScheduleAdmin)
admin.site.register(OrganizationWebpageTemplate, OrganizationWebpageTemplateAdmin)
admin.site.register(OrganizationWebpage, OrganizationWebpageAdmin)
admin.site.register(OrganizationEcardTemplate, OrganizationEcardTemplateAdmin)
admin.site.register(OrganizationEcard, OrganizationEcardAdmin)
