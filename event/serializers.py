from rest_framework import serializers
from . import models
from organization.serializers import OrganizationEventCategorySerializer,OrganizationSerializer
from users.serializers import CustomerSerializer
from organization.pcloud import getAuth
from utilitys.pCloud import uploadFile




class EventSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only =True)
    avatar = serializers.URLField()
    class Meta:
        model = models.Event
        fields = ['id','name','category','thumb','date','quotation','isActive','venue','place','latitude','longitude','avatar']


class EventCreateSerializer(serializers.ModelSerializer):
    thumbnail = serializers.FileField(required = False)
    class Meta:
        model = models.Event
        fields = ['id','organization','name','category','thumbnail','date','quotation','isActive','customer','mutuals','venue','place','latitude','longitude']

    def create(self, validated_data):
        thumb = validated_data.pop('thumbnail')
        organization = validated_data['organization'].id
        pcloudAuth = getAuth(organization)
        print(pcloudAuth)
        if pcloudAuth is not None:
            response = uploadFile(pcloudAuth,data=thumb,folderPath='/eventimage')
            if response !=400 :
                validated_data.update({'pcloudImageId':response['fileid']})
                validated_data.update({'pcloudPublicCode':response['code']})
                validated_data.update({'thumb':response['publiclink']})
        return super().create(validated_data)
    


class OrganizationEventScheduleSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField(read_only =True)
    event = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = models.OrganizationEventSchedule
        fields = ['id','organization','event','title','description','isEventDate','createdAt','scheduleAt','status']
    

class OrganizationEventScheduleCreateSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField()
    class Meta:
        model = models.OrganizationEventSchedule
        fields = ['organization_id','event','title','description','scheduleAt']



class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ['id','event','title','isSelectionEnable','isSheetPlacementEnable','maxSelectionCount','isPublic']


class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumImage
        fields = ['id','album','pcloudImageID','pcloudPublicCode','isActive','imageLink']


