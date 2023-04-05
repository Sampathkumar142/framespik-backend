from django.contrib import admin
from .models import State, Zone, Place, Avatar, TransactionMode, Music


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['id', 'state', 'title']


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'zone', 'name']


@admin.register(Avatar)
class AvatarAdmin(admin.ModelAdmin):
    list_display = ['id', 'thumb', 'pcloudImageID', 'pcloudPublicCode', 'gender']


@admin.register(TransactionMode)
class TransactionModeAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'file']
