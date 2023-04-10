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
from accounts.models import Payment,EMIPayment
from django.db.models import Q,Count
from datetime import date,timedelta,timezone
import datetime
from django.db.models.functions import ExtractMonth
from django.contrib.auth.decorators import permission_required
from utilitys.pCloud import getItemsInFolder,deleteFolder,deleteFile,createFolder,uploadFile,getAccountInfo
from .pcloud import register,getAuth
from event.serializers import OrganizationEventScheduleSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render,HttpResponse
from django.contrib.sites.models import Site





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
        

        emi = Payment.objects.filter(organization_id=organization_id).order_by('-startDate').first()
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



class OrganizationViewsSet(APIView):
    def get(self,request,*args,**kwargs):
        organization = self.request.query_params.get('organization_id',None)
        webview = self.request.query_params.get('webview',0)
        appview = self.request.query_params.get('appview',0)
        promotionalview = self.request.query_params.get('promotionview',0)
        if organization is not None:
            try:
                view,created = models.OrganizationViews.objects.get_or_create(organization_id = organization)
            except models.OrganizationViews.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
            if webview :
                view.webViews +=1
                view.save()
            if appview:
                view.appViews +=1
                view.save()
            if promotionalview:
                view.promotionalViews +=1
                view.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
              



class OrganizationWebPageTemplateViewSet(ModelViewSet):
    serializer_class = serializers.OrganizationWebPageTemplateSerializer
    queryset = models.OrganizationWebpageTemplate.objects.all()



class OrganizationWebpageViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['organization_id']
    serializer_class = serializers.OrganizationWebPageSerializer
    queryset = models.OrganizationWebpage.objects.all()





class OrganizationEcardTemplateViewSet(ModelViewSet):
    serializer_class = serializers.OrganizationEcardTemplateSerializer
    queryset = models.OrganizationEcardTemplate.objects.all()



class OrganizationEcardViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['organization_id']
    serializer_class = serializers.OrganizationEcardSerializer
    queryset = models.OrganizationEcard.objects.all()






def organizationWebPage(request,uniquecode):
    try:
        webpage =models.OrganizationWebpage.objects.select_related('organization').get(passCode = uniquecode)
        if webpage.isActive and webpage.isPublic:
            organizationandwebpagedata = models.OrganizationWebpage.get_template_data(webpage)
            organizationEcard = models.OrganizationEcard.objects.filter(organization_id=webpage.organization.id)
            current_site = Site.objects.get_current()
            domain = current_site.domain
            data = {
                'organizationandwebpagedata':organizationandwebpagedata,
                'organizationEcard' : [{'id':i.pk,'ecard_url':f'{domain}/organization/ecard/{i.passCode}'} for i in organizationEcard]
            }
            print(data)
            return render(request,'webpage.html',data)
        return HttpResponse("webpage is not Active",status = status.HTTP_423_LOCKED)
    except models.OrganizationWebpage.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)




def getOrganizationEcard(request,uniquecode):
    try: 
        organizationecard = models.OrganizationEcard.objects.select_related('organization').get(passCode = uniquecode)
        data={}
        if organizationecard.isActive :
            organizationandecarddata = models.OrganizationEcard.get_template_data(organizationecard)
            data={'organizationandecarddata':organizationandecarddata}
            print(data)
            return render(request,'ecard.html',data)
        
        else:
            return HttpResponse({"ecard is not Active"},status = status.HTTP_423_LOCKED)
    except models.OrganizationEcard.DoesNotExist :
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)