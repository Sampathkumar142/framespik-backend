from django.shortcuts import render,HttpResponse,get_object_or_404
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin
from rest_framework.generics import GenericAPIView
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When, Value, CharField
from rest_framework.views import APIView
from rest_framework.validators import ValidationError
from rest_framework.decorators import action,api_view
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from event.pagination import DefaultPagination
from django.db.models import F,Value,Case,When,Count,Sum,IntegerField,ExpressionWrapper,CharField,Q
from django.db.models import OuterRef, Subquery,CharField,Func,DecimalField,Exists
from django.db.models.functions import Coalesce
from django.contrib.sites.models import Site
import datetime
from django.conf import settings
import concurrent.futures
from django.contrib.auth.decorators import permission_required,user_passes_test,login_required



# Create your views here.


class EventViewSet(CreateModelMixin,ListModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.EventCreateSerializer
        return serializers.EventSerializer
    def get_queryset(self):
            return models.Event.objects.annotate(
    avatar=Case(
        When(customer__isnull=True, then=Value('default-avatar.png')),
        When(customer__user__isnull=True, then=Value('default-avatar.png')),
        When(customer__user__avatar__thumb__isnull=True, then=Value('default-avatar.png')),
        default='customer__user__avatar__thumb',
        output_field=CharField(),
    )
)  


        
class OrganizationEventScheduleViewSet(ModelViewSet):
     def get_serializer_class(self):
          if self.request.method =='POST':
               return serializers.OrganizationEventScheduleCreateSerializer
          return serializers.OrganizationEventScheduleSerializer
     def get_queryset(self):
          return models.OrganizationEventSchedule.objects.all()




class EventShedule(APIView):
    def post(self,request,*args,**kwargs):
        event = request.data.get('event_id')

        eventschedule = models.OrganizationEventSchedule.objects.filter(event_id = event)
        serializer = serializers.OrganizationEventScheduleSerializer(eventschedule,many=True)

        return Response(serializer.data,status=status.HTTP_200_OK)
    

class AlbumViewSet(ModelViewSet):
    def get_queryset(self):
        event = self.request.query_params.get('event_id')
        queryset = models.Album.objects.select_related('event').all()
        if event is not None:
            return queryset.filter(event_id = event)
        return queryset

    serializer_class = serializers.AlbumSerializer




class AlbumImageViewSet(ModelViewSet):
    pagination_class = DefaultPagination

    def get_queryset(self):
        album = self.request.query_params.get('album_id')
        offset = self.request.query_params.get('offset', 0)
        limit = self.request.query_params.get('limit', 10)
        queryset = models.AlbumImage.objects.select_related('album')
        if album is not None:
            queryset = queryset.filter(album_id=album)
        return queryset[int(offset):int(offset)+int(limit)]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return serializers.AlbumImageUpdateSerializer
        elif self.request.method == 'POST':
            return serializers.AlbumImageCreateSerializer
        return serializers.AlbumImageSerializer

    def update(self, request, *args, **kwargs):
        """
        Override the default update method to handle bulk updates using the `AlbumImageUpdateSerializer`.
        """
        kwargs['partial'] = True
        dataset = request.data.get('album_images')
        if not dataset:
            raise ValidationError({'album_images': 'This field is required.'})
        queryset = self.get_queryset()
        objects = []
        for item in dataset:
            pk = item.get('id', None)
            if not pk:
                raise ValidationError({'id': 'This field is required.'})
            obj = queryset.get(pk=pk)
            for i in ('isSelected','position','priority','sheetNumber','isActive'):
                setattr(obj, i, item[i])  
            obj.save()
            serializer = serializers.AlbumImageUpdateSerializer(obj)                     
            objects.append(serializer.data)
        return Response(objects,status=status.HTTP_200_OK)
            

class AlbumFaceViewSet(ModelViewSet):
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['album_id']
    def get_queryset(self):
        return models.AlbumFace.objects.all()
    def get_serializer_class(self):
        return serializers.AlbumFaceSerializer


class EventStreamViewSet(ModelViewSet):
    def get_queryset(self):
        event = self.request.query_params.get('event_id')
        queryset = models.EventStream.objects.all().prefetch_related(
            Prefetch('event', queryset=models.Event.objects.select_related('category').all()))
        if event is not None:
            return queryset.filter(event_id = event)
        return queryset

    def get_serializer_class(self):
        if self.request.method in ['POST','PUT']:
            return serializers.EventStreamCreateSerializer
        return serializers.EventStreamSerializer
    

class EventTransactionViewSet(ModelViewSet):
    def get_queryset(self):
        event = self.request.query_params.get('event_id')
        mode = self.request.query_params.get('mode_id')
        queryset = models.EventTransaction.objects.select_related('event').select_related('mode').all()
        if event is not None and mode is not None:
            return queryset.filter(event_id=event).filter(mode_id = mode)
        elif event is not None:
            return queryset.filter(event_id = event)
        elif mode is not None:
            return queryset.filter(mode_id = mode)
        return queryset
    
    def get_serializer_class(self):
        if self.request.method in ['POST','PUT','PATCH']:
            return serializers.EventTransactionCreateSerializer
        return serializers.EventTransactionSerializer
    

def getStatusOfPaymentRemainder(lastreminded):
    currentTime = datetime.datetime.now()
    print(currentTime.time())
    if lastreminded is not None:
        lastreminded = lastreminded.replace(tzinfo=None)
        time_diff = (currentTime - lastreminded).total_seconds() / 60.0
        print(time_diff)
        if time_diff < settings.MAX_GAP_FOR_PAYMENT_REMAINDER:
            return False
        return True
    return True





class EventInfoViewSet(APIView):
    def get(self,request,*args,**kwargs):
        event_id = request.query_params.get('event_id')
        
        try:
            event = models.Event.objects.select_related('category').select_related('webpage').prefetch_related(Prefetch('invitations',queryset=models.EventInvitation.objects.select_related('template').select_related('category').all())).prefetch_related(
                Prefetch('transaction',queryset=models.EventTransaction.objects.all())
            ).prefetch_related(
                Prefetch('mutuals',queryset = models.Customer.objects.all())
            ).annotate(
                albumCount=Count('album'),
                totalTransactionValue=Coalesce(Sum('transaction__value'), 0),
                hasTransactions=Count('transaction'),
                due=Case(
                    When(hasTransactions=0, then=F('quotation')),
                    default=F('quotation') - F('totalTransactionValue'),
                    output_field=DecimalField(decimal_places=2, max_digits=10)
                )
            ).get(id=event_id)

            albums = models.Album.objects.filter(event=event).prefetch_related(
                Prefetch('faces', queryset=models.AlbumFace.objects.all())
            ).prefetch_related(
                Prefetch('images',queryset=models.AlbumImage.objects.all())
            ).annotate(
                imageCount=Count('images'),
                selectedImagesCount=Count('images', filter=Q(images__isSelected=True)),
            )

            current_site = Site.objects.get_current()
            domain = current_site.domain
            webpageUrl = f"{domain}/memories/{event.webpage.passCode}"

            remainder = models.EventPaymentRemainder.objects.filter(event_id = event_id).order_by('-dateTime').first()
            if remainder is not None:
                lastPaymentReminded = remainder.dateTime
            else:
                lastPaymentReminded = None

            isPaymentRemaindable = getStatusOfPaymentRemainder(lastPaymentReminded)


            event_data = {
                'id': event.id,
                'name': event.name,
                'albumCount': event.albumCount,
                'date': event.date,
                'due': event.due,
                'quotation': event.quotation,
                'totalTransactionValue': event.totalTransactionValue,
                'hasTransactions': event.hasTransactions,
                'category': event.category.title,
                'eventwebpage':webpageUrl,
                'eventwebpagepreview':event.webpage.template.templateOverview.url,
                'webpageisActive':event.webpage.isActive,
                'webpageisPublic':event.webpage.isPublic,
                'eventinvitation':[{'templateoverview':i.template.templateOverview.url,'invitationUrl':i.template.htmlFile.url,'isActive':i.isActive,'category':i.category.title} for i in event.invitations.all()],
                'customer':{'name':event.customer.user.name,'mobile':event.customer.user.phoneNumber},
                'mutuals':[{'name':i.user.name,'mobile': i.user.phoneNumber} for i in event.mutuals.all()],
                'isPaymentRemaindable': isPaymentRemaindable,
            }

            albums_data = []
            for album in albums:
                faces = list(album.faces.values('id','faceUrl'))
                albumImages =  list(album.images.values('id','imageLink')[:4])
                albums_data.append({
                    'id': album.id,
                    'title': album.title,
                    'imagesCount': album.imageCount,
                    'selectedImagesCount': album.selectedImagesCount,
                    'albumimages': albumImages,
                    'albumfaces': faces
                })

            

            response_data = {
                'event': event_data,
                'albums': albums_data
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except models.Event.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


#------------------------event webpage-----------------------------------------------


class EventWebPageTemplateViewSet(ModelViewSet):
    serializer_class = serializers.EventWebpageTemplateSerializer
    queryset = models.EventWebpageTemplate.objects.all()


class EventWebpageViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['event_id']
    serializer_class = serializers.EventWebpageSerializer
    queryset = models.EventWebpage.objects.all()

#<---------------------------------------EventInvitationViesets------------------------>


class EventInvitationTemplateViewSet(ModelViewSet):
    serializer_class = serializers.EventInvitationTemplateSerializer
    queryset = models.EventInvitationTemplate.objects.all()


class EventInvitationViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['event_id']
    serializer_class = serializers.EventInvitationSerializer
    queryset = models.EventInvitation.objects.all()


class EventWishViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['event_id']
    serializer_class = serializers.EventWishSerializer
    queryset = models.EventWish.objects.all()



class EventpaymentRemainderViewSet(ModelViewSet):
    filter_backends=[DjangoFilterBackend]
    filterset_fields = ['event_id']
    serializer_class = serializers.EventpaymentRemainderSerializer
    queryset = models.EventPaymentRemainder.objects.all()


#**_------------------------------digital invitation viwsets----------------------->


class DigitalInvitationTemplateViewSet(ModelViewSet):
    serializer_class = serializers.DigitalInvitationTemplateSerializer
    queryset = models.DigitalInvitationTemplate.objects.all()


class DigitalInvitationLogViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event_id','customer_id']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.DigitalInvitationLogCreateSerializer
        return serializers.DigitalInvitationLogSerializer
    
    def get_queryset(self):
        queryset = models.DigitalInvitationLog.objects.select_related('event').select_related('customer').select_related('template').prefetch_related(
            Prefetch('invitations', queryset=models.DigitalInvitation.objects.prefetch_related('audient'))
        ).all()
        return queryset


class TargetedAudientViewSet(ModelViewSet):
    serializer_class = serializers.TargetedAudientSerializer
    queryset = models.TargetedAudient.objects.all()



class DigitalInvitationViewSet(ModelViewSet):
    def get_serializer_class(self):
        return serializers.DigitalInvitationSerializer
    queryset = models.DigitalInvitation.objects.all()


def eventwebpage(request,uniquecode):
    try:
        webpage =models.EventWebpage.objects.select_related('event').select_related('music').select_related('template').get(passCode = uniquecode)
        album = models.Album.objects.filter(event_id = webpage.event.id)
        invitations = models.EventInvitation.objects.select_related('category').filter(event_id = webpage.event.id)
        current_site = Site.objects.get_current()
        domain = current_site.domain
        data = {}
        if webpage.isActive and webpage.isPublic:
            eventandwebpagedata = models.EventWebpage.get_template_data(webpage)
            albumserializer = serializers.AlbumWebSerializer(album,many=True)
            data = {
                'eventandwebpagedata' :eventandwebpagedata,
                'albumdata':albumserializer.data,
                'eventinvitations':[{'invitationurl': f'{domain}/event/invite/{i.passCode}','category':i.category.title,'isActive':i.isActive} for i in invitations]
            }
            print(data)
            return render(request,'event.html',data)
        return HttpResponse("webpage is not Active",status = status.HTTP_423_LOCKED)
    except models.EventWebpage.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)


def albumimagewebpage(request,uniquecode,pk):
    try:
        webpage =models.EventWebpage.objects.select_related('event').get(passCode = uniquecode)
        images = models.AlbumImage.objects.filter(images__event_id =webpage.event.id).filter(album_id = pk).values('pk','imageLink','isActive')
        print(images.exists())
        data ={}
        if images.exists():
            if webpage.isActive:
                imagesserializer = [{'id':i['pk'],'imageLink':i['imageLink'],'isActive':i['isActive']} for i in images]
                data.update({"albumdata": imagesserializer})
                print(data)
                return render(request,'album.html',data)
            return HttpResponse("webpage is not Active",status = status.HTTP_423_LOCKED)
        else:
            return HttpResponse({"album is Empty"},status = status.HTTP_404_NOT_FOUND)

    except models.EventWebpage.DoesNotExist:
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)



def getEventInvitation(request,uniquecode):
    try: 
        eventinvitation = models.EventInvitation.objects.select_related('event').select_related('category').select_related('music').select_related('template').get(passCode = uniquecode)
        data={}
        if eventinvitation.isActive :
            invitationdata = models.EventInvitation.get_template_data(eventinvitation)
            data={'invitationdata':invitationdata}
            print(data)
            return render(request,'invitation.html',data)
        
        else:
            return HttpResponse({"invitation is not Active"},status = status.HTTP_423_LOCKED)
    except models.EventInvitation.DoesNotExist :
        return HttpResponse(status=status.HTTP_400_BAD_REQUEST)



def has_permission(user, view_func):
    def wrapper(request, *args, **kwargs):
        album_id = kwargs.get('album_id')
        event_id = kwargs.get('event_id')
        album = get_object_or_404(models.Album, id=album_id, event_id=event_id)
        customer_id =[ i.id for i in album.event.customer.all()]
        if album.isPublic and (album.event.user == user or user.id in customer_id) :
            return view_func(request, album_id=album_id, event_id=event_id, *args, **kwargs)
        else:
            return render(request, 'access_denied.html')
    return wrapper


@login_required(login_url='/login/')
@user_passes_test(lambda u: has_permission(u, imageSelection))
def imageSelection(request, album_id, event_id):
    album = get_object_or_404(models.Album, id=album_id, event_id=event_id)
    images = album.images.all()
    imagesdata = serializers.AlbumImageSerializer(images, many=True)
    print(imagesdata.data)
    return render(request, 'image_selection.html', {'album': album, 'images': imagesdata.data})
