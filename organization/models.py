from core.models import Zone
from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator
from django.db import models
import uuid
import base64
from django.contrib.auth.hashers import make_password


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
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    proprietorImage = models.ImageField(upload_to=user_directory_path, null=True,blank =True)

    proprietor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

    address = models.TextField()
    isMaintainingOffice = models.BooleanField()
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)

    whatsapp = models.CharField(max_length=10)
    phoneNumber = models.CharField(max_length=13)

    facebook = models.TextField(null=True, blank=True)
    instagram = models.TextField(null=True, blank=True)
    youtube = models.TextField(null=True, blank=True)

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
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT,null=True,blank =True)
    customPlan = models.ForeignKey(CustomPlan, on_delete=models.PROTECT,null=True,blank =True)

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
class OrganizationWebpageTemplate(models.Model):
    htmlFileName = models.CharField(max_length=1000)
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    templateName = models.CharField(max_length=100)




# ____________________________ Organization Webpage _________________________
class OrganizationWebpage(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    isActive = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    template = models.ForeignKey(
        OrganizationWebpageTemplate, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # create a UUID based on the primary key
        name = str(self.pk).encode('utf-8')
        namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
        uuid5 = uuid.uuid5(namespace, name)
        self.uuid = base64.b64encode(uuid5.bytes)[:8].decode('utf-8')
        super().save(*args, **kwargs)




# ______________________ Organization Ecard Template ________________________________
class OrganizationEcardTemplate(models.Model):
    htmlFileName = models.CharField(max_length=1000)
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    templateName = models.CharField(max_length=100)


# ____________________________ Organization Ecard _________________________
class OrganizationEcard(models.Model):
    uuid = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False)
    isActive = models.BooleanField(default=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    template = models.ForeignKey(
        OrganizationEcardTemplate, on_delete=models.PROTECT)

    def save(self, *args, **kwargs):
        # create a UUID based on the primary key
        name = str(self.pk).encode('utf-8')
        namespace = uuid.UUID('00000000-0000-0000-0000-000000000000')
        uuid5 = uuid.uuid5(namespace, name)
        self.uuid = base64.b64encode(uuid5.bytes)[:8].decode('utf-8')
        super().save(*args, **kwargs)







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