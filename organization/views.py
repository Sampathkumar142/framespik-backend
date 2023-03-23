from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from . import models
from . import serializers
from event.models import Event,OrganizationEventSchedule
from rest_framework.response import Response
from rest_framework import status
from utilitys import pCloud
from  rest_framework.views import APIView
from affiliate.models import OrganizationCommision
from accounts.models import EMI,EMIPayment
from django.db.models import Q,Count
from datetime import date,timedelta,timezone
import datetime
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import permission_required
from utilitys.pCloud import getItemsInFolder,deleteFolder,deleteFile,createFolder,uploadFile,getAccountInfo
from .pcloud import register,getAuth
from event.serializers import OrganizationEventScheduleSerializer






class OrganizationViewSet(CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    queryset = models.Organization.objects.all()

    def get_serializer_class(self):
        if self.request.method =="POST":
            return serializers.OrganizationCreateSerializer
        return serializers.OrganizationSerializer
    def get_serializer_context(self):
        return {'request':self.request}
    



class OrganizationPortifolioViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrganizationPortifolioCreateSerializer
        return serializers.OrganizationPortfolioSerializer
    
    def get_queryset(self):
        return models.OrganizationPortfolio.objects.all()
    
       
        

        

    

class OrganizationInfoViewSet(APIView):
    def get(self,request,*args,**kwargs):
        print(register('praveensampathkumar.parvathini@gmail.com','sampath@123'))
        return Response("ok")
        
    def post(self,request,*args,**kwargs):
        organization_id = request.data.get('organization_id')
        dict = {}
        organization = models.Organization.objects.select_related('credential').select_related('views').filter(id = organization_id).get()
        if organization is not None:
            dict.update({'organization_title':organization.name})
            dict.update({'events_count':organization.eventsCount})
            dict.update({'albums_count':organization.albumsCount})
            dict.update({'streams_count':organization.streamsCount})
            dict.update({'invitation_count':organization.invitationsCount})
            dict.update({'plan_amount':organization.credential.amount})
            dict.update({'nextRenewableDate':organization.credential.nextRenewableDate})
            dict.update({'emiPayable':organization.emiPayable})
            dict.update({'webviews':organization.views.webViews})
            dict.update({'pomotionviews':organization.views.promotionalViews})
            dict.update({'appViews':organization.views.appViews})
            info = getAccountInfo(organization.credential.email,organization.credential.password)
            if info['result'] ==0:
                percentage = (info['usedquota']/info['quota'])*100
                dict.update({'pcloudSpaceUsed':percentage})

    
        commision = OrganizationCommision.objects.filter(organization_id = organization_id)
        if commision.exists():
             dict.update({"commission": [{"revenue": emi.commision, "isSettled": emi.isSettled} for emi in commision]})


        event = Event.objects.select_related('customer').filter(organization_id = organization_id).order_by('-date')
        if event.exists():
            dict.update({"events":[{"id":i.id,"name":i.name,"category":i.category.title,"date":i.date,"thumb":i.thumb,"avatar":i.customer.user.avatar.thumb} for i in event[:4]]})
        

        emi = EMI.objects.filter(organization_id=organization_id).order_by('-startDate').first()
        if organization is not None and emi is not None:
            emipayment = EMIPayment.objects.filter(emi_id=emi.id).order_by('paymentDate').filter(Q(paymentDate__month=date.today().month) & Q(status='DUE'))
            if organization.emiPayable == True:
                if "emi" not in dict:
                    dict.update({"emi": []})
                if emipayment.exists():
                    emipayment_list = [{"amount": emipayment.amount, "next_payment_date": emipayment.paymentDate,"status":emipayment.status} for emipayment in emipayment]
                    dict["emi"].extend(emipayment_list)


        current_year = datetime.datetime.now().year
        count_list = [0] * 12  # initialize the list with zeros for all months
        if event.exists():
            event = event.filter(date__year = current_year)
            count_per_month = event.annotate(month=ExtractMonth('date')).values_list('month').annotate(count=Count('id')).order_by('month')
            for month, count in count_per_month:
                count_list[month-1] = count
            dict.update({"events_done":count_list})
        else:
            dict.update({"events_done":count_list})


        return Response(dict,status=status.HTTP_200_OK)

        


        
class OrganizationScheduleViewSet(ModelViewSet):
     def get_serializer_class(self):
          if self.request.method =='POST':
               return serializers.OrganizationScheduleCreateSerializer
          return serializers.OrganizationScheduleSerializer
     def get_queryset(self):
          return models.OrganizationSchedule.objects.all()
     

class FeatureCategoryViewSet(ModelViewSet):
    def get_serializer_class(self):
        return serializers.FeatureCategorySerializer
    queryset = models.FeatureCategory.objects.all()


class FeatureViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method =="POST":
            return serializers.FeatureCreateSerializer
        return serializers.FeatureSerializer
    queryset = models.Feature.objects.all()


class PlanViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method =="POST":
            return serializers.PlanCreateSerializer
        return serializers.PlanSerializer
    queryset = models.Plan.objects.all()


class CustomPlanViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method =="POST":
            return serializers.CustomPlanCreateSerializer
        return serializers.CustomPlanSerializer
    queryset = models.CustomPlan.objects.all()




class ScheduleView(APIView):
    def post(self,request,*args,**kwargs):
        data = {}
        organization = request.data.get('organization_id')
        organizationschedule = models.OrganizationSchedule.objects.filter(organization_id = organization)
        organizationeventschedule = OrganizationEventSchedule.objects.filter(organization_id = organization)
        if organizationschedule is not None:
            organizationserializer = serializers.OrganizationScheduleSerializer(organizationschedule,many=True)
            data.update({'schedules':organizationserializer.data})
        if organizationeventschedule is not None:
            organizationeventserializer = OrganizationEventScheduleSerializer(organizationeventschedule,many =True)
            data.update({'eventschedules':organizationeventserializer.data})
        return Response(data,status=status.HTTP_200_OK)
