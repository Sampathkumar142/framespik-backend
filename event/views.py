from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet,GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,DestroyModelMixin
from rest_framework.generics import GenericAPIView
from . import serializers
from . import models
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, When, Value, CharField
from rest_framework.views import APIView

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
    queryset = models.Album.objects.all()
    serializer_class = serializers.AlbumSerializer


class AlbumImageViewSet(ModelViewSet):
     queryset = models.AlbumImage.objects.all()
     serializer_class = serializers.AlbumImageSerializer     