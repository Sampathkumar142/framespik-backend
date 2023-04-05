from django.contrib import admin
from .models import Event, Album, AlbumImage, AlbumFace, EventTransaction, EventStream, EventWebpageTemplate, EventWebpage
from .models import (
    EventInvitationTemplate,
    EventInvitation,
    EventWish,
    EventPaymentRemainder,
    DigitalInvitationTemplate,
    OrganizationEventSchedule
)



@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'organization', 'customer', 'date', 'time', 'isActive')
    list_filter = ('isActive', 'organization', 'customer', 'category')
    search_fields = ('name', 'venue', 'place__name')


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'isSelectionEnable', 'isSheetPlacementEnable', 'maxSelectionCount', 'isPublic')
    list_filter = ('event', 'isSelectionEnable', 'isSheetPlacementEnable', 'isPublic')
    search_fields = ('title', 'event__name')


@admin.register(AlbumImage)
class AlbumImageAdmin(admin.ModelAdmin):
    list_display = ('album', 'isActive', 'isSelected', 'sheetNumber', 'position', 'priority')
    list_filter = ('isActive', 'isSelected')
    search_fields = ('album__title', 'album__event__name', 'imageLink', 'faceCharacters')


@admin.register(AlbumFace)
class AlbumFaceAdmin(admin.ModelAdmin):
    list_display = ('album', 'faceUrl', 'imageCode', 'publicCode')
    list_filter = ('album',)
    search_fields = ('album__title', 'faceUrl', 'imageCode', 'publicCode')


@admin.register(EventTransaction)
class EventTransactionAdmin(admin.ModelAdmin):
    list_display = ('event', 'value', 'mode', 'date')
    list_filter = ('event', 'mode')


@admin.register(EventStream)
class EventStreamAdmin(admin.ModelAdmin):
    list_display = ('event', 'youtubeLink')
    list_filter = ('event',)


@admin.register(EventWebpageTemplate)
class EventWebpageTemplateAdmin(admin.ModelAdmin):
    list_display = ('templateName', 'uploadedAt', 'get_file_url')


@admin.register(EventWebpage)
class EventWebpageAdmin(admin.ModelAdmin):
    list_display = ('event', 'template', 'music', 'isActive')
    list_filter = ('event', 'isActive')
    search_fields = ('event__name', 'template__templateName')



class EventInvitationTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'templateName', 'uploadedAt']
    search_fields = ['templateName']
    
class EventInvitationAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'template', 'isActive', 'category']
    search_fields = ['event__name', 'template__templateName']
    
class EventWishAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'name', 'mobile']
    search_fields = ['event__name', 'name', 'mobile']
    
class EventPaymentRemainderAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'dateTime']
    search_fields = ['event__name']
    
class DigitalInvitationTemplateAdmin(admin.ModelAdmin):
    list_display = ['id', 'templateName', 'uploadedAt']
    search_fields = ['templateName']


class OrganizationEventScheduleAdmin(admin.ModelAdmin):
    list_display = ('title', 'organization', 'event', 'scheduleAt', 'isEventDate', 'status')

admin.site.register(OrganizationEventSchedule, OrganizationEventScheduleAdmin)


admin.site.register(EventInvitationTemplate, EventInvitationTemplateAdmin)
admin.site.register(EventInvitation, EventInvitationAdmin)
admin.site.register(EventWish, EventWishAdmin)
admin.site.register(EventPaymentRemainder, EventPaymentRemainderAdmin)
admin.site.register(DigitalInvitationTemplate, DigitalInvitationTemplateAdmin)