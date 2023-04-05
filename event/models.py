import os
from django.db import models
from django.conf import settings
from users.models import Customer
from core.models import Place, TransactionMode, Music
from organization.models import Organization, OrganizationEventCategory
from .validators import FileValidator
import random
import string



# ____________________________ Events  ____________________
def generate_unique_digit(length=6):
    while True:
        random_string = ''.join(random.choices(string.digits, k=length))
        if not Event.objects.filter(securityKey=random_string).exists():
            return random_string

class Event(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        OrganizationEventCategory, on_delete=models.PROTECT)
    thumb = models.URLField(null =True,blank=True)
    pcloudImageId = models.CharField(max_length=50, null=True,blank=True)
    pcloudPublicCode = models.CharField(max_length=50,null=True,blank =True)
    date = models.DateField()
    time = models.TimeField(null=True,blank=True)
    quotation = models.IntegerField()
    isActive = models.BooleanField()


    securityKey = models.IntegerField(unique=True,default=generate_unique_digit)

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    mutuals = models.ManyToManyField(Customer, related_name='mutualEvents',blank=True)

    venue = models.CharField(max_length=70)
    place = models.ForeignKey(Place, on_delete=models.PROTECT)
    latitude = models.CharField(max_length=30)
    longitude = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.name


    def save(self, *args, **kwargs):
        is_new = self.pk is None
        # call parent class's save method
        super(Event, self).save(*args, **kwargs)
        if is_new:
            # create a new instance of OrganizationEventSchedule
            schedule = OrganizationEventSchedule.objects.create(
                organization_id=self.organization.id,
                title=self.name,
                isEventDate=True,
                scheduleAt=self.date,
                event_id = self.pk,
                scheduleTime = self.time|None
            )
            event_webpage = EventWebpage.objects.create(
                event_id = self.pk,
                template = EventWebpageTemplate.objects.first(),
                music  = Music.objects.first()
            )
        return self


# ______________________________ Even Albums _______________________
class Album(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT,related_name='album')
    title = models.CharField(max_length=25)
    isSelectionEnable = models.BooleanField(default=False)
    isSheetPlacementEnable = models.BooleanField(default=False)
    maxSelectionCount = models.IntegerField(null=True, blank=True)
    isPublic = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

# ______________________________ Event Album Images _____________________
class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT,related_name='images')
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    isSelected = models.BooleanField(default=False)
    imageLink = models.URLField(max_length=1638)
    sheetNumber = models.PositiveSmallIntegerField(null=True, blank=True)
    position = models.CharField(max_length=1, null=True, blank=True)
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    faceCharacters = models.TextField(null=True, blank=True)


class AlbumFace(models.Model):
    album = models.ForeignKey(Album,on_delete=models.CASCADE,related_name='faces')
    faceUrl = models.URLField(max_length=250)
    imageCode = models.IntegerField()
    publicCode = models.IntegerField()

# _____________________________ Event Transactions _____________________
class EventTransaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT,related_name='transaction')
    value = models.IntegerField()
    mode = models.ForeignKey(TransactionMode, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)

    
    # **************** Payment Gateway *******************


# ____________________________ Event Streaming _________________________
class EventStream(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    youtubeLink = models.URLField()


# ____________________________ Event Web Template _________________________


def get_file_path(instance, filename):
    return f'eventtemplates/webpagetemplate/{filename}'


class EventWebpageTemplate(models.Model):
    templateOverview = models.ImageField(upload_to=f'eventtemplates/webtemplateoverview')
    templateName = models.CharField(max_length=100)
    htmlFile = models.FileField(upload_to=get_file_path,validators=[FileValidator(['html'])])
    uploadedAt = models.DateTimeField(auto_now_add = True)



    # def save(self, *args, **kwargs):
    #     condition = not  self.templateName
    #     super(EventWebpageTemplate, self).save(*args, **kwargs)
    #     if condition:
    #         self.templateName = os.path.basename(self.htmlFile.name) 
    #         self.save(update_fields=['templateName'])

    def __str__(self) -> str:
        return self.htmlFile.url
    
    
    def get_file_url(self):
        return self.htmlFile.url

    
    def delete(self, *args, **kwargs):
        # Delete the file from the storage backend
        self.templateOverview.storage.delete(self.templateOverview.name)
        self.htmlFile.storage.delete(self.htmlFile.name)

        super(EventWebpageTemplate, self).delete(*args, **kwargs)

# ____________________________ Event Webpage _________________________
def generate_unique_string(length=8):
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not EventWebpage.objects.filter(passCode=random_string).exists():
            return random_string

class EventWebpage(models.Model):
    event = models.OneToOneField(Event, on_delete=models.CASCADE,related_name='webpage')
    template = models.ForeignKey(
        EventWebpageTemplate, on_delete=models.PROTECT,related_name='template')
    isActive = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)
    passCode = models.CharField(max_length =8,unique=True,default=generate_unique_string)
    music = models.ForeignKey(
        Music, on_delete=models.SET_NULL, null=True, blank=True)
    heroImage1 = models.URLField(max_length=500)
    heroImage2 = models.URLField(max_length=500,null=True,blank=True)
    heroImage3 = models.URLField(max_length=500,null=True,blank=True)
    heroImage4 = models.URLField(max_length=500,null=True,blank=True)

    def get_template_data(self):
        data = {
            'event_name': self.event.name,
            'event_date': self.event.date,
            'event_venue': self.event.venue,
            'event_place': self.event.place.name,
            'event_latitude': self.event.latitude,
            'event_longitude': self.event.longitude,
            'hero_images': [
                self.heroImage1, self.heroImage2, self.heroImage3,
                self.heroImage4
            ],
            'template':self.template.htmlFile.url if self.template.htmlFile.url else None,
            'music_url': self.music.file.url if self.music.file.url else None,
            'passCode':self.passCode
        }
        
        # add more conditions for other event categories as needed
        return data


# ____________________________ Event Invitation Template _________________________
def get_invitation_template_path(instance, filename):
    return f'eventtemplates/invitationtemplate/{filename}'


class EventInvitationTemplate(models.Model):
    templateOverview = models.ImageField(upload_to=f'eventtemplates/invitationtemplateoverview')
    templateName = models.CharField(max_length=100)
    htmlFile = models.FileField(upload_to=get_invitation_template_path,validators=[FileValidator(['html'])])
    uploadedAt = models.DateTimeField(auto_now_add = True)


    # def save(self, *args, **kwargs):
    #     condition = not  self.templateName
    #     super(EventInvitationTemplate, self).save(*args, **kwargs)
    #     if condition:
    #         self.templateName = os.path.basename(self.htmlFile.name) 
    #         self.save(update_fields=['templateName'])

    def __str__(self) -> str:
        return self.templateName
    
    def delete(self, *args, **kwargs):
        # Delete the file from the storage backend
        self.templateOverview.storage.delete(self.templateOverview.name)
        self.htmlFile.storage.delete(self.htmlFile.name)

        super(EventWebpageTemplate, self).delete(*args, **kwargs)



# ____________________________ Event Invitation Template _________________________
def generate_unique_string_invitation(length=8):
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not EventInvitation.objects.filter(passCode=random_string).exists():
            return random_string



class EventInvitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='invitations')
    template = models.ForeignKey(
        EventInvitationTemplate, on_delete=models.PROTECT)
    isActive = models.BooleanField(default=True)
    music = models.ForeignKey(
        Music, on_delete=models.SET_NULL, null=True, blank=True)
    passCode = models.CharField(max_length = 8,unique=True,default=generate_unique_string_invitation)
    category = models.ForeignKey(
        OrganizationEventCategory, on_delete=models.PROTECT, related_name='events')
    birthday_person_name = models.CharField(max_length=250,null=True, blank=True)
    groom_name = models.CharField(max_length=250,null =True, blank=True)
    bride_name = models.CharField(max_length=250,null=True, blank=True)
    heroImage1 = models.URLField(max_length=500)
    heroImage2 = models.URLField(max_length=500,null=True,blank=True)
    heroImage3 = models.URLField(max_length=500,null=True,blank=True)
    heroImage4 = models.URLField(max_length=500,null=True,blank=True)
    heroImage5 = models.URLField(max_length=500,blank=True,null=True)
    heroImage6 = models.URLField(max_length=500,blank=True,null=True)
    heroImage7 = models.URLField(max_length=500,null=True,blank=True)
    
    def get_template_data(self):
        data = {
            'event_name': self.event.name,
            'event_date': self.event.date,
            'event_venue': self.event.venue,
            'event_place': self.event.place.name,
            'event_latitude': self.event.latitude,
            'event_longitude': self.event.longitude,
            'hero_images': [
                self.heroImage1, self.heroImage2, self.heroImage3,
                self.heroImage4, self.heroImage5, self.heroImage6, self.heroImage7
            ],
            'template':self.template.htmlFile.url if self.template.htmlFile.url else None,
            'music_url': self.music.file.url if self.music.file.url else None,
            'passCode':self.passCode
        }
        if self.category.title == 'birthday':
            data['birthday_person_name'] = self.birthday_person_name
        elif self.category.title == 'Wedding':
            data['groom_name'] = self.groom_name
            data['bride_name'] = self.bride_name
        # add more conditions for other event categories as needed
        return data





# ___________________________ Event Wishes ______________________________
class EventWish(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    message = models.CharField(max_length=2000)
    mobile = models.IntegerField()


# ___________________________ Event Payment Remainders ________________________
class EventPaymentRemainder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,related_name='paymentremainder')
    dateTime = models.DateTimeField(auto_now_add=True)



#  _________________________ Bulk Invitation Template ______________________________


def get_digital_invitation_template_path(instance,filename):
    return f'eventtemplates/digitalinvitationtemplate/{filename}'


class DigitalInvitationTemplate(models.Model):
    templateOverview = models.ImageField(upload_to=f'eventtemplates/digitalinvitationtemplateoverview')
    templateName = models.CharField(max_length=100)
    htmlFile = models.FileField(upload_to=get_digital_invitation_template_path,validators=[FileValidator(['html'])])
    uploadedAt = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        condition = not  self.templateName
        super(DigitalInvitationTemplate, self).save(*args, **kwargs)
        if condition:
            self.templateName = os.path.basename(self.htmlFile.name) 
            self.save(update_fields=['templateName'])

    def __str__(self) -> str:
        return self.templateName

    def delete(self, *args, **kwargs):
        # Delete the file from the storage backend
        self.templateOverview.storage.delete(self.templateOverview.name)
        self.htmlFile.storage.delete(self.htmlFile.name)

        super(DigitalInvitationTemplate, self).delete(*args, **kwargs)


# ___________________________ Event Digital Invitation Log ____________________________
class DigitalInvitationLog(models.Model):
    """
    it record who, when made an invitation action and
    for what event the invitation send.
    """
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT)
    dateTime = models.DateTimeField(auto_now_add=True)
    template = models.ForeignKey(
        DigitalInvitationTemplate, on_delete=models.PROTECT)
    isWhatsappInvitation = models.BooleanField()
    isMessageInvitation = models.BooleanField()
    price = models.IntegerField()



# ___________________________ Targeted Audience Stack ____________________________
class TargetedAudient(models.Model):
    """
    it stores the data of the targeted audient with no repeat
    """
    # name of the targeted audient
    audientName = models.CharField(max_length=120, null=True, blank=True)
    phoneNumber = models.CharField(max_length=12)
    dateTime = models.DateTimeField(auto_now_add=True)


# ___________________________ Invitation Structure ________________________________
class DigitalInvitation(models.Model):
    """
    it stores the structure of how the invitation is sent
    and to whom it is sent.
    """
    log = models.ForeignKey(DigitalInvitationLog, on_delete=models.CASCADE,related_name='invitations')
    audient = models.ForeignKey(TargetedAudient, on_delete=models.PROTECT)
    dateTime = models.DateTimeField(auto_now_add=True)




class OrganizationEventSchedule(models.Model):
    organization = models.ForeignKey(Organization,on_delete =models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    isEventDate = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    scheduleAt = models.DateField()
    scheduleTime = models.TimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    




