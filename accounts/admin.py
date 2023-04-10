
from django.contrib import admin
from .models import EMIPayment, Payment

@admin.register(EMIPayment)
class EMIPaymentAdmin(admin.ModelAdmin):
    list_display = ('emi', 'paymentDate', 'amount', 'status')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('organization', 'amount', 'emiEnabled','tenure', 'startDate', 'endDate','date','expireDate')
