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
        thumb =None
        if 'thumbnail' in validated_data.keys():
            thumb = validated_data.pop('thumbnail')
        organization = validated_data['organization'].id
        pcloudAuth = getAuth(organization)
        print(pcloudAuth)
        if pcloudAuth is not None and thumb is not None :
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
        fields = ['id','organization_id','event','title','description','scheduleAt']



class AlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Album
        fields = ['id','event','title','isSelectionEnable','isSheetPlacementEnable','maxSelectionCount','isPublic']


class AlbumImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumImage
        fields = ['id','album','isActive','imageLink','isSelected','position','priority','sheetNumber']

        

class AlbumImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumImage
        fields = ['id','album','pcloudImageID','pcloudPublicCode','imageLink']




class AlbumImageUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.AlbumImage
        fields = ['id','isSelected','position','priority','sheetNumber','isActive']



class AlbumFaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AlbumFace
        fields = ['id','album','faceUrl','imageCode','publicCode']
        
class EventStreamDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = models.Event
        fields = ['id','name','category','thumb','date','quotation','isActive','venue','place','latitude','longitude']




class EventStreamSerializer(serializers.ModelSerializer):
    event = EventStreamDetailSerializer(read_only =True)
    class Meta:
        model = models.EventStream
        fields = ['id','event','youtubeLink']


class EventStreamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventStream
        fields = ['id','event','youtubeLink']


class EventTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventTransaction
        fields = ['id','event','value','mode','date']



class EventTransactionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventTransaction
        fields = ['id','event','value','mode']







#event webpage template  serializers



class EventWebpageTemplateSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(read_only =True)
    class Meta:
        model = models.EventWebpageTemplate
        fields = ['id','templateName','templateOverview','htmlFile','uploadedAt']



class EventWebpageSerializer(serializers.ModelSerializer):
    template = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = models.EventWebpage
        fields = ['id','event','template','isActive','isPublic','passCode','music']





#event invitation template serializers


class EventInvitationTemplateSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(read_only =True)
    class Meta:
        model = models.EventInvitationTemplate
        fields = ['id','templateName','templateOverview','htmlFile','uploadedAt']



class EventInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventInvitation
        fields = ['id','event', 'template', 'isActive', 'music', 'category', 'birthday_person_name', 'groom_name', 'bride_name', 'heroImage1', 'heroImage2', 'heroImage3', 'heroImage4', 'heroImage5', 'heroImage6', 'heroImage7']




class EventWishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventWish
        fields = ['id','event','name','message']




class EventpaymentRemainderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventPaymentRemainder
        fields = ['id','event','dateTime']



# digital bulk invitation serializers


class DigitalInvitationTemplateSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(read_only =True)
    class Meta:
        model = models.DigitalInvitationTemplate
        fields = ['id','templateName','templateOverview','htmlFile','uploadedAt']



class TargetedAudientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TargetedAudient
        fields = ['id','audientName','phoneNumber','dateTime']
    

        

class DigitalInvitationSerializer(serializers.ModelSerializer):
    audient = TargetedAudientSerializer(read_only =True)    
    class Meta:
        model = models.DigitalInvitation
        fields = ['id','log','audient','dateTime']

class DigitalInvitationLogSerializer(serializers.ModelSerializer):
    invitations = DigitalInvitationSerializer(many=True, read_only=True)
    
    class Meta:
        model =models.DigitalInvitationLog
        fields = ['id','event','customer','dateTime','template','isWhatsappInvitation','isMessageInvitation','price','invitations']



class DigitalInvitationLogCreateSerializer(serializers.ModelSerializer):
    audient = TargetedAudientSerializer(many =True,write_only =True)

    class Meta:
        model =models.DigitalInvitationLog
        fields = ['id','event','customer','dateTime','template','isWhatsappInvitation','isMessageInvitation','price','audient']


    def create(self, validated_data):
        audients = validated_data.pop('audient')
        log = super().create(validated_data)
        for audient in audients:
            obj,created = models.TargetedAudient.objects.get_or_create(phoneNumber = audient['phoneNumber'])
            obj.audientName = audient['audientName']
            obj.save()
            invitationobj = models.DigitalInvitation.objects.create(log=log, audient = obj)
        return log





class AlbumWebSerializer(serializers.ModelSerializer):
    imagesCount = serializers.IntegerField(read_only =True) 
    class Meta:
        model = models.Album
        fields = ['id','event','title','maxSelectionCount','isPublic','imagesCount']