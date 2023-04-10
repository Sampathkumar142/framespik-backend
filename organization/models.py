from core.models import Zone
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
import uuid
import base64
from django.contrib.auth.hashers import make_password
from event.validators import FileValidator
import random
import string




class FeatureCategory(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.title


class Feature(models.Model):
    htmlId = models.CharField(max_length=100)
    category = models.ForeignKey(FeatureCategory,on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.name



class Plan(models.Model):
    name = models.CharField(max_length=255)
    features = models.ManyToManyField(Feature)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name
    

class CustomPlan(models.Model):
    name = models.CharField(max_length=255)
    features = models.ManyToManyField(Feature)
    price = models.DecimalField(max_digits=6, decimal_places=2)


    def __str__(self):
        return self.name
    

    @classmethod
    def create_with_price(cls, name, features):
        total_price = sum(feature.price for feature in features)
        feature_plan = cls.objects.create(name=name, price=total_price)
        feature_plan.features.set(features)
        return feature_plan
    



# ____________________________ Category of Organization Ex: Event-Management, Photography, Editor, Event manager + Photographer ____________________
class OrganizationCategory(models.Model):
    isFaceRecognitionEnable = models.BooleanField()
    isProductionToolsEnable = models.BooleanField()
    title = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title


# ____________________________ Organizations Event Categories (Sub-Category),  ____________________
class OrganizationEventCategory(models.Model):
    """
    we list these Subcategories at creating events,
    and portfolio images accordingly.
    """
    description = models.TextField()
    isFaceRecognitionEnable = models.BooleanField()
    thumbnail = models.URLField(unique=True)
    title = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.title



# ____________________________ Organization Tier Ex: Bronze, Silver, Gold, Platinum ____________________
class OrganizationTier(models.Model):
    """
    when ever the Organizer adds an event we calculate the average quotation of
    all his events (including present adding event) and set the tire accordingly.
    the avgQuotation value of tire he fits in should be <= calculated avg value.
    """
    avgQuotation = models.BigIntegerField()
    title = models.CharField(max_length=60)

    def __str__(self) -> str:
        return self.title


# ____________________________  Organization Ex: Framespik Organizations, Framespik Studios, Framespik Editing Room ____________________

def user_directory_path(instance, filename):
    return f'proprieterimage/{filename}'


class Organization(models.Model):
    id = models.UUIDField(primary_key= True,default=uuid.uuid4)
    category = models.ForeignKey(
        OrganizationCategory, on_delete=models.PROTECT)
    name = models.CharField(max_length=80)
    tier = models.ForeignKey(OrganizationTier, on_delete=models.PROTECT)
    # proprietor Image
    proprietorImage = models.ImageField(upload_to=user_directory_path, null=True,blank =True)

    proprietor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    studioLogo  = models.ImageField(upload_to='organization/studiologo',null=True,blank =True)
    studioPhoto = models.ImageField(upload_to='organization/studiophoto',null=True,blank =True)
    address = models.TextField()
    isMaintainingOffice = models.BooleanField()
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

    whatsapp = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=13)

    facebook = models.URLField(max_length = 400,null=True, blank=True)
    instagram = models.URLField(max_length = 400,null=True, blank=True)
    youtube = models.URLField(max_length =400,null=True, blank=True)

    albumsCount = models.PositiveBigIntegerField(default=0)
    eventsCount = models.PositiveBigIntegerField(default=0)
    invitationsCount = models.PositiveBigIntegerField(default=0)
    streamsCount = models.PositiveBigIntegerField(default=0)
    emiPayable = models.BooleanField(default=False)
    isCustomPlan = models.BooleanField(default=False)
    bankAccountNumber = models.CharField(max_length=20, validators=[
        RegexValidator(r'^[0-9]{9,18}$', 'Invalid bank account number'),
        MinLengthValidator(9),
        MaxLengthValidator(18)
    ], null=True, blank=True)

    ifscCode = models.CharField(max_length=11, validators=[
        RegexValidator(r'^[A-Z]{4}[0-9]{7}$', 'Invalid IFSC code')
    ], null=True, blank=True)

    nameAsPerBank = models.CharField(max_length=255, null=True, blank=True)
    bankName = models.CharField(max_length=255, null=True, blank=True)

    ACTIVE = 'A'
    INACTIVE = 'I'
    HOLD = 'H'
    STATUS_CHOICE = {
        (ACTIVE, 'Active'),
        (INACTIVE, 'In Active'),
        (HOLD, 'Hold'),
    }
    status = models.CharField(
        max_length=1, choices=STATUS_CHOICE, default=ACTIVE)
    lastUpdated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name



# ______________________ Organization Portfolio ________________________________
class OrganizationPortfolio(models.Model):
    category = models.ForeignKey(
        OrganizationEventCategory, on_delete=models.PROTECT)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    thumb = models.URLField(unique=True)
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=3000)




# ____________________________ Organization Web Template _________________________
def get_file_path(instance, filename):
    return f'organizationtemplates/webpagetemplate/{filename}'


class OrganizationWebpageTemplate(models.Model):
    templateOverview = models.ImageField(upload_to=f'organizationtemplates/webtemplateoverview')
    htmlFile = models.FileField(upload_to=get_file_path,validators=[FileValidator(['html'])])
    templateName = models.CharField(max_length=100)
    uploadedAt = models.DateTimeField(auto_now_add=True)

    def get_file_url(self):
        return self.htmlFile.url
    
    def __str__(self) -> str:
        return self.htmlFile.url

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        # Delete the file from the storage backend
        self.templateOverview.storage.delete(self.templateOverview.name)
        self.htmlFile.storage.delete(self.htmlFile.name)

        super(OrganizationWebpageTemplate, self).delete(*args, **kwargs)




# ____________________________ Organization Webpage _________________________
def generate_unique_string_webpage(length=8):
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not OrganizationWebpage.objects.filter(passCode=random_string).exists():
            return random_string

class OrganizationWebpage(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    isActive = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)
    passCode = models.CharField(max_length = 8,unique=True,default=generate_unique_string_webpage)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    template = models.ForeignKey(
        OrganizationWebpageTemplate, on_delete=models.PROTECT)

    def get_template_data(self):
        data = {
            'organization_name': self.organization.name,
            'organization_proprietorImage': self.organization.proprietorImage.url if self.organization.proprietorImage else None,
            'organization_studiologo': self.organization.studioLogo.url if self.organization.studioLogo else None,
            'organization_studiophoto': self.organization.studioPhoto.url if self.organization.studioPhoto else None,
            'organization_address': self.organization.address,
            'organization_isMaintainableOffice': self.organization.isMaintainingOffice,
            'organization_lattitude': self.organization.latitude,
            'organization_longitude': self.organization.longitude,
            'organization_zone': self.organization.zone.title,
            'organization_state':self.organization.zone.state.title,
            'organization_whatsapp':self.organization.whatsapp,
            'organization_phonenumber':self.organization.phoneNumber,
            'organization_facebook':self.organization.facebook,
            'organization_youtube':self.organization.youtube,
            'organization_status':self.organization.status,
            'organization_proprietor_name':self.organization.proprietor.name,
            'organization_proprietor_phonenumber':self.organization.proprietor.phoneNumber,
            'organization_proprietor_email':self.organization.proprietor.email if self.organization.proprietor.email else None,
            'template':self.template.htmlFile.url if self.template.htmlFile.url else None,
            'isActive':self.isActive,
            'isPublic':self.isPublic
        }
        return data


# ______________________ Organization Ecard Template ________________________________
def get_ecard_path(instance, filename):
    return f'organizationtemplates/ecardtemplates/{filename}'


class OrganizationEcardTemplate(models.Model):
    htmlFile = models.FileField(upload_to=get_ecard_path,validators=[FileValidator(['html'])])
    templateName = models.CharField(max_length=100)
    uploadedAt = models.DateTimeField(auto_now_add = True)
    templateOverview = models.ImageField(upload_to=f'organizationtemplates/ecardoverview')

    def __str__(self) -> str:
        return self.templateName
    
    def delete(self, *args, **kwargs):
        # Delete the file from the storage backend
        self.templateOverview.storage.delete(self.templateOverview.name)
        self.htmlFile.storage.delete(self.htmlFile.name)

        super(OrganizationEcardTemplate, self).delete(*args, **kwargs)




# ____________________________ Organization Ecard _________________________

def generate_unique_string_ecard(length=8):
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not OrganizationEcard.objects.filter(passCode=random_string).exists():
            return random_string





class OrganizationEcard(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    isActive = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    template = models.ForeignKey(
        OrganizationEcardTemplate, on_delete=models.PROTECT)
    passCode = models.CharField(max_length = 8,unique=True,default=generate_unique_string_ecard)

  

    def get_template_data(self):
        data = {
            'organization_name': self.organization.name,
            'organization_proprietorImage': self.organization.proprietorImage.url if self.organization.proprietorImage else None,
           'organization_studiologo': self.organization.studioLogo.url if self.organization.studioLogo else None,
            'organization_studiophoto': self.organization.studioPhoto.url if self.organization.studioPhoto else None,
            'organization_address': self.organization.address,
            'organization_isMaintainableOffice': self.organization.isMaintainingOffice,
            'organization_lattitude': self.organization.latitude,
            'organization_longitude': self.organization.longitude,
            'organization_zone': self.organization.zone.title,
            'organization_state':self.organization.zone.state.title,
            'organization_whatsapp':self.organization.whatsapp,
            'organization_phonenumber':self.organization.phoneNumber,
            'organization_facebook':self.organization.facebook,
            'organization_youtube':self.organization.youtube,
            'organization_status':self.organization.status,
            'organization_proprietor_name':self.organization.proprietor.name,
            'organization_proprietor_phonenumber':self.organization.proprietor.phoneNumber,
            'organization_proprietor_email':self.organization.proprietor.email if self.organization.proprietor.email else None,
            'template':self.template.htmlFile.url if self.template.htmlFile.url else None,
            'isActive':self.isActive
    }
        return data





class OrganizationViews(models.Model):
    webViews = models.PositiveBigIntegerField(default=0)
    appViews = models.PositiveBigIntegerField(default=0)
    promotionalViews = models.PositiveBigIntegerField(default=0)
    organization = models.OneToOneField(Organization,models.PROTECT,related_name='views')


 


class PcloudAccountPlan(models.Model):
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=8,decimal_places=2)
    tenure = models.IntegerField()
    storage = models.DecimalField(max_digits=8,decimal_places=2)





class OrganizationPcloudCredentials(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=150)
    plan = models.ForeignKey(PcloudAccountPlan,on_delete=models.PROTECT)
    auth = models.CharField(max_length=225,null=True,blank=True)
    nextRenewableDate = models.DateField(null=True,blank =True)
    organization = models.OneToOneField(Organization,on_delete=models.CASCADE,related_name='credential') 
    lastLogin = models.DateField(null=True,blank=True)


    




class OrganizationSchedule(models.Model):
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank =True)
    createdAt = models.DateTimeField(auto_now=True)
    scheduledAt = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title