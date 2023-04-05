
from django.contrib import admin
from .models import EMIPayment, EMI

@admin.register(EMIPayment)
class EMIPaymentAdmin(admin.ModelAdmin):
    list_display = ('emi', 'paymentDate', 'amount', 'status')

@admin.register(EMI)
class EMIAdmin(admin.ModelAdmin):
    list_display = ('organization', 'amount', 'tenure', 'installmentAmount', 'startDate', 'endDate')
