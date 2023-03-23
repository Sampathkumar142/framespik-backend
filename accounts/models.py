from django.db import models
from datetime import date,timedelta
from organization.models import Organization

# Create your models here.

class EMIPayment(models.Model):
    emi = models.ForeignKey('EMI', on_delete=models.CASCADE,related_name='paymentrecord')
    paymentDate = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=(('paid', 'Paid'), ('due', 'Due')),default='due')





class EMI(models.Model):
    organization = models.ForeignKey(Organization,on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()
    installmentAmount = models.DecimalField(max_digits=10, decimal_places=2)
    startDate = models.DateField()
    endDate = models.DateField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.installmentAmount = self.calculate_installment_amount()
            startDate = date.today()
            endDate = startDate + timedelta(days=self.tenure * 30)
            self.start_date = startDate
            self.end_date = endDate
            super().save(*args, **kwargs)
            self.create_emipayments()

    def create_emipayments(self):
        paymentDate = self.startDate
        balance = self.amount
        for i in range(self.tenure):
            principal_amount = self.installment_amount 
            balance = balance - principal_amount
            EMIPayment.objects.create(
                emi=self,
                paymentDate=paymentDate,
                amount=balance,
            )
            payment_date = payment_date + timedelta(days=30)






