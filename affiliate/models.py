from django.db import models
from users.models import Affiliate
from organization.models import Organization
from users.models import Customer
from event.models import DigitalInvitationLog


class AffiliateConnection(models.Model):
    affiliate  = models.ForeignKey(Affiliate,on_delete=models.PROTECT)
    organization = models.OneToOneField(Organization,on_delete=models.PROTECT)
    commision = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    isSettled = models.BooleanField(default=False)

class AffiliateSettled(models.Model):
    affiliate = models.ForeignKey(Affiliate,on_delete=models.PROTECT)
    value = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    totalConnects = models.PositiveIntegerField()
    



class OrganizationCommision(models.Model):
    organization  = models.ForeignKey(Organization,on_delete=models.PROTECT)
    commision = models.PositiveIntegerField()
    product = models.ForeignKey(DigitalInvitationLog,on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    isSettled = models.BooleanField(default=False)



class OrganizationSettled(models.Model):
    organization = models.ForeignKey(Organization,on_delete=models.PROTECT) 
    value = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    totalConnects = models.PositiveIntegerField()
