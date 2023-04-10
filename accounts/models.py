from django.db import models
from datetime import date,timedelta
from organization.models import Organization,Plan,CustomPlan
from django.utils import timezone
from decimal import Decimal

# Create your models here.

class EMIPayment(models.Model):
    emi = models.ForeignKey('Payment', on_delete=models.CASCADE,related_name='paymentrecord')
    paymentDate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(('paid', 'Paid'), ('due', 'Due')),default='Due')





class Payment(models.Model):
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE,related_name='payment')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    emiEnabled = models.BooleanField(default=False)
    plan = models.ForeignKey(Plan, on_delete=models.PROTECT,null=True,blank =True)
    customPlan = models.ForeignKey(CustomPlan, on_delete=models.PROTECT,null=True,blank =True)
    tenure = models.IntegerField()
    startDate = models.DateField()
    endDate = models.DateField()
    date = models.DateField(default=timezone.now)
    expireDate = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk and self.emiEnabled == True:
            startDate = date.today()
            endDate = startDate + timedelta(days=self.tenure * 30)
            self.startDate = startDate
            self.endDate = endDate
            self.expireDate = date +  timedelta(days=self.tenure *365)
            super().save(*args, **kwargs)
            self.create_emipayments()
        else:
            super().save(*args,**kwargs)

    def create_emipayments(self):
        payment_date = self.startDate

        balance = self.amount
        for i in range(self.tenure):
            principal_amount = self.amount/self.tenure
            balance = balance - principal_amount
            EMIPayment.objects.create(
                emi=self,
                paymentDate=payment_date,
                amount=balance,
            )
            payment_date = payment_date + timedelta(days=30)




