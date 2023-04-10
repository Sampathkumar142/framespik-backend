from rest_framework import serializers
from djoser.serializers import UserSerializer as BaseUserSerializer,UserCreateSerializer as BaseUserCreateSerializer
from . import models
from core.models import Avatar
from organization.serializers import OrganizationSerializer
from django.db.models import Q





#<----------------------------- USER SERIALIZERS ---------------------------------->
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id','phoneNumber','email','name','avatar','dateOfBirth']
    



class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','phoneNumber','email','name','isWebTourDone','isSoftwareTourDone','isAffiliate','isOrganizationAdmin','isCustomer','isEmailVerified','isOrganizationStaff','avatar','isMarketEmployee','dateOfBirth','isAppTourDone','is_active']





#<--------------------------------------OrganizerUSER ------------------------------->  
class OrganizationUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only =True)
    organization = OrganizationSerializer(read_only =True)
    class Meta:
        model = models.OrganizationUser
        fields =['user','organization','whatsapp']




class OrganizationUserCreateSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.IntegerField(write_only =True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(),required = False)
    dateOfBirth = serializers.DateField(required=False)
    name = serializers.CharField(max_length = 100,write_only =True)
    email = serializers.EmailField(write_only =True)

    class Meta:
        model = models.OrganizationUser
        fields = ['phoneNumber','avatar','dateOfBirth','email','name','organization','whatsapp']

    
    def create(self, validated_data):
        try:
            user= models.User.objects.get(Q(phoneNumber=validated_data['phoneNumber'])|Q(email = validated_data['email']))
            user.isOrganizationStaff = True
            user.save()
        except models.User.DoesNotExist :
            user = models.User.objects.create_user(phoneNumber=validated_data['phoneNumber'],email=validated_data['email'],name = validated_data['name'],isOrganizationStaff= True)
            if 'avatar' in list(validated_data.keys()):
                user.avatar = validated_data['avatar']
            if 'dateofBirth' in list(validated_data.keys()):
                user.dateOfBirth = validated_data.pop('dateOfBirth')
            user.save()
        finally:
            if 'avatar' in list(validated_data.keys()):
                validated_data.pop('avatar')
            if 'dateOfBirth' in list(validated_data.keys()):
                validated_data.pop('dateOfBirth')
            validated_data.pop('email')
            validated_data.pop('name')
            validated_data.pop('phoneNumber')
        validated_data['user'] = user

        return super().create(validated_data)
    



#<----------------------------------Affiliate User ---------------------------->

class AffiliateSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only =True)
    class Meta:
        model = models.Affiliate
        fields =['id','user','commissionPercentage','joinedDate','revenue','referCode']







class AffiliateCreateSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.IntegerField(write_only =True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(),required = False)
    dateOfBirth = serializers.DateField(required=False)
    name = serializers.CharField(max_length = 100,write_only =True)
    email = serializers.EmailField(write_only =True)
    user = serializers.PrimaryKeyRelatedField(read_only =True)
    class Meta:
        model = models.Affiliate
        fields = ['phoneNumber','avatar','dateOfBirth','name','email','user']
    def create(self, validated_data):
        try:
            user= models.User.objects.get(Q(phoneNumber=validated_data['phoneNumber'])|Q(email = validated_data['email']))
            user.name =validated_data['name']
            user.email = validated_data['email'] 
            user.isAffiliate = True
            user.save()
        except models.User.DoesNotExist :
            user = models.User.objects.create_user(phoneNumber=validated_data['phoneNumber'],email=validated_data['email'],name = validated_data['name'],isAffiliate= True)
            if 'avatar' in list(validated_data.keys()):
                user.avatar = validated_data['avatar']
            if 'dateofBirth' in list(validated_data.keys()):
                user.dateOfBirth = validated_data.pop('dateOfBirth')
            user.save()
        finally:
            if 'avatar' in list(validated_data.keys()):
                validated_data.pop('avatar')
            if 'dateOfBirth' in list(validated_data.keys()):
                validated_data.pop('dateOfBirth')
            validated_data.pop('email')
            validated_data.pop('name')
            validated_data.pop('phoneNumber')
        validated_data['user'] = user

        return super().create(validated_data)




#<-------------------------------- Customer ---------------------------->
class CustomerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only =True)
    organization = OrganizationSerializer(many = True,read_only = True)
    class Meta:
        model = models.Customer
        fields = ['id','user','organization','isVerified']



class CustomerCreateSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.IntegerField(write_only =True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(),required = False)
    name = serializers.CharField(max_length = 100,write_only =True)
    class Meta:
        model = models.Customer
        fields = ['phoneNumber','avatar','name','organization']

    def create(self, validated_data):
        try:
            user= models.User.objects.get(Q(phoneNumber=validated_data['phoneNumber']))
            user.isCustomer = True
            user.avatar = validated_data['avatar']
            user.name = validated_data['name']
            user.save()
        except models.User.DoesNotExist :
            user = models.User.objects.create_user(phoneNumber=validated_data['phoneNumber'],name = validated_data['name'],isCustomer= True)
            if  'avatar' in list(validated_data.keys()):
                user.avatar = validated_data['avatar']
            user.save()
        finally:
            if  'avatar' in list(validated_data.keys()):
                validated_data.pop('avatar')
            validated_data.pop('name')
            validated_data.pop('phoneNumber')
        validated_data['user'] = user
        organizations = validated_data.pop('organization',[])
        for organization in organizations: 
            try:
                customer1 = models.Customer.objects.get(Q(organization__id =organization.id) & Q(user_id = user.id))
                organizations.remove(organization)
            except models.Customer.DoesNotExist:
                pass
        if len(organizations)>0:
            customer = models.Customer.objects.create(**validated_data)
            for organization in organizations:
                customer.organization.add(organization)
            return customer
        return customer1
   



#<-------------------------------EMPLOYEE ---------------------------->

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only =True)
    role = serializers.StringRelatedField(read_only = True)
    
    class Meta:
        model = models.Employee
        fields = ['address','isManager','joinedDate','phoneNumber','role','user','aadharNumber','panNumber','bankAccountNumber','ifscCode','nameAsPerBank','bankName','bloodGroup']



class EmployeeCreateSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.IntegerField(write_only =True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(),required = False)
    dateOfBirth = serializers.DateField(required=False)
    name = serializers.CharField(max_length = 100,write_only =True)
    email = serializers.EmailField(write_only =True)
    class Meta:
        model = models.Employee
        fields = ['address','interviewSummary','isManager','phoneNumber','role','salary','aadharNumber','panNumber','bankAccountNumber','ifscCode','nameAsPerBank','bankName','bloodGroup','phoneNumber','avatar','dateOfBirth','name','email']


    def create(self, validated_data):
        try:
            user= models.User.objects.get(Q(phoneNumber=validated_data['phoneNumber'])|Q(email = validated_data['email']))
            user.isEmployee = True
            user.email = validated_data['email']
            user.name = validated_data['name']
            user.save()
        except models.User.DoesNotExist :
            user = models.User.objects.create_user(phoneNumber=validated_data['phoneNumber'],email=validated_data['email'],name = validated_data['name'],isEmployee= True)
            if 'avatar' in list(validated_data.keys()):
                user.avatar = validated_data['avatar']
            if 'dateofBirth' in list(validated_data.keys()):
                user.dateOfBirth = validated_data.pop('dateOfBirth')
            user.save()
        finally:
            if 'avatar' in list(validated_data.keys()):
                validated_data.pop('avatar')
            if 'dateOfBirth' in list(validated_data.keys()):
                validated_data.pop('dateOfBirth')
            validated_data.pop('email')
            validated_data.pop('name')
            validated_data.pop('phoneNumber')
        validated_data['user'] = user
        return super().create(validated_data)




#<--------------------------------------Marketer------------------------>
class MarketerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only =True)
    class Meta:
        model = models.Marketer
        fields = ['address','isManager','joinedDate','isEligibleToTravel','user','aadharNumber','panNumber','bankAccountNumber','ifscCode','nameAsPerBank','bankName','bloodGroup','zone']



class MarketerCreateSerializer(serializers.ModelSerializer):
    phoneNumber = serializers.IntegerField(write_only =True)
    avatar = serializers.PrimaryKeyRelatedField(
        queryset=Avatar.objects.all(),required = False)
    dateOfBirth = serializers.DateField(required=False)
    name = serializers.CharField(max_length = 100,write_only =True)
    email = serializers.EmailField(write_only =True)
    class Meta:
        model = models.Marketer
        fields = ['address','interviewSummary','isManager','whatsapp','isEligibleToTravel','salary','aadharNumber','panNumber','bankAccountNumber','ifscCode','nameAsPerBank','bankName','bloodGroup','zone','phoneNumber','avatar','dateOfBirth','name','email']

    def create(self, validated_data):
        try:
            user= models.User.objects.get(Q(phoneNumber=validated_data['phoneNumber'])|Q(email = validated_data['email']))
            user.isMarketer = True
            user.email =  validated_data['email']
            user.name = validated_data['name']
            user.save()
        except models.User.DoesNotExist :
            user = models.User.objects.create_user(phoneNumber=validated_data['phoneNumber'],email=validated_data['email'],name = validated_data['name'],isMarketer= True)
            if 'avatar' in list(validated_data.keys()):
                user.avatar = validated_data['avatar']
            if 'dateofBirth' in list(validated_data.keys()):
                user.dateOfBirth = validated_data.pop('dateOfBirth')
            user.save()
        finally:
            if 'avatar' in list(validated_data.keys()):
                validated_data.pop('avatar')
            if 'dateOfBirth' in list(validated_data.keys()):
                validated_data.pop('dateOfBirth')
            validated_data.pop('email')
            validated_data.pop('name')
            validated_data.pop('phoneNumber')
        validated_data['user'] = user
        zones = validated_data.pop('zone',[])
        marketer = models.Marketer.objects.create(**validated_data)
        for zone in zones:
            marketer.zone.add(zone) 
        return marketer



