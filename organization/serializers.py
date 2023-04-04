from rest_framework import serializers
from .  import models 
from core.models import Avatar
from users.models import User, OrganizationUser
from django.db.models import Q
from django.conf import settings
from core.serializers import ZoneSerializer
from users.models import Affiliate
from affiliate.models import AffiliateConnection
from .pcloud import  register as pcloudRegistration,getAuth
from utilitys.pCloud import getItemsInFolder,deleteFolder,deleteFile,createFolder,uploadFile
from rest_framework.response import Response
from rest_framework import status


class OrganizationCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationCategory
        fields = ['id','title','isProductionToolsEnable','isFaceRecognitionEnable']


class OrganizationEventCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationEventCategory
        fields = ['id','description','isFaceRecognitionEnable','thumbnail','title']

class OrganizationSerializer(serializers.ModelSerializer):
    category = OrganizationCategorySerializer(read_only = True)
    tier = serializers.StringRelatedField(read_only = True)
    zone = ZoneSerializer(read_only = True)
    class Meta:
        model = models.Organization
        fields = ['id','category','name','tier','pcloudImageID','pcloudPublicCode','address','isMaintainingOffice','latitude','longitude','zone','whatsapp','phoneNumber','facebook','instagram','youtube','albumsCount','eventsCount','invitationsCount','streamsCount','status','lastUpdated']


class OrganizationCreateSerializer(serializers.ModelSerializer):
    proprietor = serializers.PrimaryKeyRelatedField(read_only=True)


    # fields to create a proprietor
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(), write_only=True)
    dateOfBirth = serializers.DateField(write_only=True)
    email = serializers.EmailField(write_only=True)
    proprietorName = serializers.CharField(max_length=25, write_only=True)
    proprietorPhoneNumber = serializers.CharField(
        max_length=10, write_only=True)
    proprietorWhatsappNumber = serializers.CharField(
        max_length=10, write_only=True)

    referCode = serializers.CharField(max_length = 6,write_only = True,required = False)

    #field to pcloud plan
    pcloudPlan = serializers.PrimaryKeyRelatedField(queryset = models.PcloudAccountPlan.objects.all(),write_only =True)
    class Meta:
        model = models.Organization
        fields = ['category', 'name', 'proprietor','proprietorImage'
                  , 'address', 'isMaintainingOffice', 'latitude',
                  'longitude', 'zone', 'whatsapp', 'phoneNumber',
                  'facebook', 'instagram', 'youtube',
                  'plan',
                  'bankAccountNumber', 'ifscCode', 'nameAsPerBank', 'bankName',
                  'avatar', 'dateOfBirth', 'email', 'proprietorName', 'proprietorPhoneNumber', 'proprietorWhatsappNumber','tier','referCode','pcloudPlan']

    def create(self, validated_data):
        try:
            user = User.objects.get(Q(phoneNumber=validated_data['proprietorPhoneNumber']))
            user.isOrganizationAdmin = True
            user.isOrganizationStaff = True
            user.save()
        except User.DoesNotExist:
            user = User()
            user.avatar = validated_data['avatar']
            user.dateOfBirth = validated_data['dateOfBirth']
            user.email = validated_data['email']
            user.name = validated_data['proprietorName']
            user.phoneNumber = validated_data['proprietorPhoneNumber']
            user.isOrganizationAdmin = True
            user.isOrganizationStaff = True
            user.save()
        finally:

            # Cleaning validated_data to create organization
            pcloudplan = validated_data.pop('pcloudPlan')
            plan = validated_data['plan']
            proprietorImage = validated_data.pop('proprietorImage')
            validated_data.pop('avatar')
            validated_data.pop('dateOfBirth')
            email =validated_data.pop('email')
            validated_data.pop('proprietorName')
            proprietorPhoneNumber = validated_data.pop('proprietorPhoneNumber')
            validated_data.pop('proprietorWhatsappNumber')
            referCode =None
            if 'referCode' in validated_data.keys():
                referCode = validated_data.pop('referCode')
        validated_data['proprietor'] = user
        organization = models.Organization.objects.create(**validated_data)
        password = f"{proprietorPhoneNumber}@framespik"
        response = pcloudRegistration(email,password)
        if response == 200:
            credential = models.OrganizationPcloudCredentials.objects.create(email =email,password=password,organization_id = organization.id,plan=pcloudplan)
            # if credential is not None:
            #     auth = getAuth(organization.id)
            #     data = getItemsInFolder(auth,path="/")
            #     if data['result'] == 0:
            #         for folder in data['metadata']['contents']:
            #             if folder['isfolder'] == True :
            #                 if 'ispublic'  in folder.keys():
            #                     pass
            #                 else:
            #                     deleteFolder(auth,folder['folderid'])
            #             else:
            #                 deleteFile(auth,folder['fileid'])
            #     createFolder(auth,path='/',name='albums')
            #     createFolder(auth,path='/',name='streams')
            #     createFolder(auth,path='/',name='faces')
            #     createFolder(auth,path='/',name='portfolio')   
            #     createFolder(auth,path='/',name='sharecards') 
            #     createFolder(auth,path='/',name='eventimage')  
                
        try:
            affiliate = Affiliate.objects.get(referCode = referCode)
            commission = (plan.price + pcloudplan.amount) * (affiliate.commissionPercentage)/100
            instance1 = AffiliateConnection.objects.create(affiliate_id = affiliate.id,organization_id = organization.id,commision=commission)
        except Affiliate.DoesNotExist:
            pass
            
        return organization






class OrganizationPortfolioSerializer(serializers.ModelSerializer):
    category = OrganizationEventCategorySerializer(read_only = True)
    class Meta:
        model = models.OrganizationPortfolio
        fields = ['id','category','organization','thumb']



class OrganizationPortifolioCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationPortfolio
        fields = ['category','organization','thumb','pcloudImageID','pcloudPublicCode']



class OrganizationScheduleSerializer(serializers.ModelSerializer):
    organization = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = models.OrganizationSchedule
        fields = ['id','organization','title','description','createdAt','scheduledAt','status']


class OrganizationScheduleCreateSerializer(serializers.ModelSerializer):
    organization_id = serializers.UUIDField()
    class Meta:
        model = models.OrganizationSchedule
        fields = ['organization_id','title','description','scheduledAt']
    


class FeatureCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FeatureCategory
        fields = '__all__'

class FeatureSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only =True)
    class Meta:
        model = models.Feature
        fields = ['id','htmlId','category','name','price']



class FeatureCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Feature
        fields = ['htmlId','category','name','price']




class PlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many = True,read_only =True)
    class Meta:
        model = models.Plan
        fields = ['id','name','features','price']





class PlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = ['name','features','price']



class CustomPlanSerializer(serializers.ModelSerializer):
    features = FeatureSerializer(many = True,read_only =True)
    class Meta:
        model = models.Plan
        fields = ['id','name','features','price']





class CustomPlanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Plan
        fields = ['name','features']

    def create(self, validated_data):
        customplan = models.CustomPlan.create_with_price(name=validated_data['name'],features=validated_data['features'])
        return customplan
    

class OrganizationWebPageTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationWebpageTemplate
        fields = ['id','templateName','templateOverview','htmlFile','uploadedAt']


class OrganizationWebPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationWebpage
        fields = ['uuid','organization','template','isActive','isPublic','passCode']



class OrganizationEcardTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationEcardTemplate
        fields = ['id','templateName','templateOverview','htmlFile','uploadedAt']



class OrganizationEcardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OrganizationEcard
        fields = ['uuid','organization','template','isActive','passCode']
