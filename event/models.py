from django.db import models
from django.conf import settings
from users.models import Customer
from core.models import Place, TransactionMode, Music
from organization.models import Organization, OrganizationEventCategory


# ____________________________ Events  ____________________
class Event(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    category = models.ForeignKey(
        OrganizationEventCategory, on_delete=models.PROTECT)
    thumb = models.URLField(null =True,blank=True)
    pcloudImageId = models.CharField(max_length=50, null=True,blank=True)
    pcloudPublicCode = models.CharField(max_length=50,null=True,blank =True)
    date = models.DateField()
    quotation = models.IntegerField()
    isActive = models.BooleanField()

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    mutuals = models.ManyToManyField(Customer, related_name='mutualEvents')

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
                event_id = self.pk
            )
        return self


# ______________________________ Even Albums _______________________
class Album(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    title = models.CharField(max_length=25)
    isSelectionEnable = models.BooleanField(default=False)
    isSheetPlacementEnable = models.BooleanField(default=False)
    maxSelectionCount = models.IntegerField(null=True, blank=True)
    isPublic = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.title

# ______________________________ Event Album Images _____________________
class AlbumImage(models.Model):
    album = models.ForeignKey(Album, on_delete=models.PROTECT)
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    isSelected = models.BooleanField(default=False)
    imageLink = models.URLField()
    sheetNumber = models.PositiveSmallIntegerField(null=True, blank=True)
    position = models.CharField(max_length=1, null=True, blank=True)
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    faceCharacters = models.TextField(null=True, blank=True)


# class AlbumFaces(models.Model):
#      = models.

# _____________________________ Event Transactions _____________________
class EventTransaction(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    value = models.IntegerField()
    mode = models.ForeignKey(TransactionMode, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now=True)
    # **************** Payment Gateway *******************


# ____________________________ Event Streaming _________________________
class EventStream(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    youtubeLink = models.URLField()


# ____________________________ Event Web Template _________________________
class EventWebpageTemplate(models.Model):
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    templateName = models.CharField(max_length=100)
    htmlFileName = models.CharField(max_length=1000)


# ____________________________ Event Webpage _________________________
class EventWebpage(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    template = models.ForeignKey(
        EventWebpageTemplate, on_delete=models.PROTECT)
    isActive = models.BooleanField(default=True)
    isPublic = models.BooleanField(default=True)
    passCode = models.PositiveSmallIntegerField()
    music = models.ForeignKey(
        Music, on_delete=models.SET_NULL, null=True, blank=True)


# ____________________________ Event Invitation Template _________________________
class EventInvitationTemplate(models.Model):
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)
    templateName = models.CharField(max_length=100)
    htmlFileName = models.CharField(max_length=1000)


# ____________________________ Event Invitation Template _________________________
class EventInvitation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    template = models.ForeignKey(
        EventInvitationTemplate, on_delete=models.PROTECT)
    isActive = models.BooleanField(default=True)
    music = models.ForeignKey(
        Music, on_delete=models.SET_NULL, null=True, blank=True)


# ___________________________ Event Wishes ______________________________
class EventWish(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    message = models.CharField(max_length=2000)


# ___________________________ Event Payment Remainders ________________________
class EventPaymentRemainder(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    dateTime = models.DateTimeField(auto_now_add=True)


#  _________________________ Bulk Invitation Template ______________________________
class DigitalInvitationTemplate(models.Model):
    template = models.CharField(max_length=500)


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
    log = models.ForeignKey(DigitalInvitationLog, on_delete=models.CASCADE)
    audient = models.ForeignKey(TargetedAudient, on_delete=models.PROTECT)
    dateTime = models.DateTimeField(auto_now_add=True)




class OrganizationEventSchedule(models.Model):
    organization = models.ForeignKey(Organization,on_delete =models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    isEventDate = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now=True)
    scheduleAt = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    



