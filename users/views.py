from  rest_framework.views import APIView
from .models import User,customerOtpStack,OrganizationUser,Affiliate,Customer,Employee,Marketer
import random
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timedelta
from rest_framework.viewsets import ModelViewSet,GenericViewSet
from . import serializers
from rest_framework.decorators import action
from djoser.views import UserViewSet as BaseUserViewSet
from django.shortcuts import get_object_or_404
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin
from rest_framework.generics import GenericAPIView,CreateAPIView


class UserViewSet(BaseUserViewSet):
    http_method_names = ['get','put']
  
    @action(["get"], detail=False)
    def me(self, request, *args, **kwargs):
        try:
            user = User.objects.get(id=int(request.user.id))
        except User.DoesNotExist:
            return Response({'User Not exist'},status=status.HTTP_404_NOT_FOUND)
        if request.method == "GET":
            serializer = serializers.UserSerializer(user)
            response = serializer.data
            if user.isCustomer:
                try:
                    customer= Customer.objects.get(user_id=request.user.id)
                    serializer = serializers.CustomerSerializer(customer)
                    response['customer'] = serializer.data
                    response['customer'].pop('user')
                except Customer.DoesNotExist :
                    pass

            if user.isAffiliate:
                try:
                    affiliate = Affiliate.objects.get(user_id=request.user.id)
                    serializer = serializers.AffiliateSerializer(affiliate)
                    response['affiliate'] = serializer.data
                    response['affiliate'].pop('user')
                except Affiliate.DoesNotExist:
                    pass



            if user.isMarketEmployee:
                try:
                    marketer = Marketer.objects.get(user_id = request.user.id)
                    serializer = serializers.MarketerSerializer(marketer)
                    response['marketer'] = serializer.data
                    response['marketer'].pop('user')
                except Marketer.DoesNotExist:
                    pass

            if user.isOrganizationStaff:
                try:
                    organizationUser = OrganizationUser.objects.get(user_id = request.user.id)
                    serializer = serializers.OrganizationUserSerializer(organizationUser)
                    response['organizationUser'] = serializer.data
                    response['organizationUser'].pop('user')
                except OrganizationUser.DoesNotExist:
                    pass
                
            return Response(response,status=status.HTTP_200_OK)








def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
                }



class CustomerViewSet(CreateModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CustomerCreateSerializer
        elif self.request.method == 'PUT':
            return serializers.CustomerSerializer
        return serializers.CustomerSerializer    
    queryset = Customer.objects.select_related('user').prefetch_related('organization').all()

    @action(detail =False,methods=['GET','PUT'])
    def me(self,request):
        try:
            customer =  Customer.objects.get(user_id=request.user.id)
        except Customer.DoesNotExist :
            return Response({'Your not an customer to any organization'},status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = serializers.CustomerSerializer(customer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = serializers.CustomerCreateSerializer(customer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
         
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(phoneNumber =request.data['phoneNumber'])
        customer = Customer.objects.get(user_id = user.id)
        serializer1 = serializers.CustomerSerializer(customer)
        
        return Response(serializer1.data, status=status.HTTP_201_CREATED, headers=headers)



class SendOtp(APIView):
    def post(self,request,*args,**kwargs):
        phone_number = request.data.get('phone')
        if phone_number:
            phone = str(phone_number)
            otp=random.randrange(1000,9999)
            print(otp)
            # otp = send_otp(phone)
            if otp:
                print(datetime.now())
                five_minutes_ago = datetime.now() - timedelta(minutes=5)
                print(five_minutes_ago)
                customerOtpStack.objects.filter(dateTime__lt= five_minutes_ago).delete()
                customerOtpStack.objects.create(phoneNumber = phone,otp = otp)
                return Response({"Otp sent Sucessfull"},status = status.HTTP_200_OK)
            else:
                return Response({"Not sent"},status=status.HTTP_400_BAD_REQUEST)
                
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class VerifyOtp(APIView):
    def post(self,request,*args,**kwargs):
        phone = request.data.get('phone',False)
        otp = request.data.get('otp',False)

        if phone and otp:
            five_minutes_ago = datetime.now() - timedelta(minutes=5)
            customerOtpStack.objects.filter(dateTime__lt= five_minutes_ago).delete()
            obj = customerOtpStack.objects.filter(phoneNumber = phone)
            if obj is not None:
                for i in obj:
                    if  i.otp == otp:
                        try:
                            user = User.objects.get(phoneNumber = phone)
                            try:
                                customer = Customer.objects.get(user_id =user.id)
                                if  customer.isVerified is False :
                                    customer.isVerified = True
                                    customer.save()
                            except Customer.DoesNotExist:
                                customer = Customer.objects.create(user_id = user.id,isVerified = True)
                        except User.DoesNotExist:
                            user =None
                        if user is None:
                            # User does not exist, create a new account
                            user = User.objects.create_user(phoneNumber=phone,isCustomer = True)
                            if user :
                                Customer.objects.create(user_id = user.id,isVerified = True)
                        customerOtpStack.objects.filter(phoneNumber=phone).delete()
                        return Response(get_tokens_for_user(user))
                else:
                    return Response({"Invalid Otp "},status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"Invalid number"},status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({"Invalid Request"},status=status.HTTP_400_BAD_REQUEST)
            
            
             



class OrganizationUserViewSet(CreateModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.OrganizationUserCreateSerializer
        elif self.request.method == 'PUT':
            return serializers.OrganizationUserSerializer
        elif self.request.method == 'PATCH':
            return serializers.OrganizationUserSerializer
        return serializers.OrganizationUserSerializer    
    queryset = OrganizationUser.objects.select_related('user').all()

    @action(detail =False,methods=['GET','PUT','PATCH'])
    def me(self,request):
        try:
            organizationUser =  OrganizationUser.objects.get(user_id=request.user.id)
        except OrganizationUser.DoesNotExist :
            return Response({'You are not belongs any organization'},status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = serializers.OrganizationUserSerializer(organizationUser)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = serializers.OrganizationUserSerializer(organizationUser,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = serializers.OrganizationUserSerializer(organizationUser,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)




class AffiliateViewSet(CreateModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AffiliateCreateSerializer
        elif self.request.method == 'PUT':
            return serializers.AffiliateSerializer
        return serializers.AffiliateSerializer    
    queryset = Affiliate.objects.select_related('user').all()

    @action(detail =False,methods=['GET','PUT'])
    def me(self,request):
        try:
            affiliate =  Affiliate.objects.get(user_id=request.user.id)
        except Affiliate.DoesNotExist :
            return Response({'Your not an Affiliate'},status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = serializers.AffiliateSerializer(affiliate)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = serializers.AffiliateCreateSerializer(affiliate,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(phoneNumber =request.data['phoneNumber'])
        affiliate = Affiliate.objects.get(user_id = user.id)
        serializer1 = serializers.AffiliateSerializer(affiliate)
        
        return Response(serializer1.data, status=status.HTTP_201_CREATED, headers=headers)





        

class EmployeeViewSet(CreateModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.EmployeeCreateSerializer
        elif self.request.method == 'PUT':
            return serializers.EmployeeSerializer
        return serializers.EmployeeSerializer    
    queryset = Employee.objects.all()

    @action(detail =False,methods=['GET','PUT'])
    def me(self,request):
        try:
            employee =  Employee.objects.get(user_id=request.user.id)
        except Employee.DoesNotExist :
            return Response({'your  not an Employee'},status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = serializers.EmployeeSerializer(employee)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = serializers.EmployeeCreateSerializer(employee,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(phoneNumber =request.data['phoneNumber'])
        employee = Employee.objects.get(user_id = user.id)
        serializer1 = serializers.EmployeeSerializer(employee)
        
        return Response(serializer1.data, status=status.HTTP_201_CREATED, headers=headers)
        


class MarketerViewSet(CreateModelMixin,GenericViewSet):
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.MarketerCreateSerializer
        elif self.request.method == 'PUT':
            return serializers.MarketerSerializer
        return serializers.MarketerSerializer    
    queryset = Marketer.objects.select_related('user').all()

    @action(detail =False,methods=['GET','PUT','PATCH'])
    def me(self,request):
        try:
            marketer =  Marketer.objects.get(user_id=request.user.id)
        except Marketer.DoesNotExist :
            return Response({'Your are not an Marketer'},status=status.HTTP_404_NOT_FOUND)
        if request.method == 'GET':
            serializer = serializers.MarketerSerializer(marketer)
            return Response(serializer.data)
        
        elif request.method == 'PUT':
            serializer = serializers.MarketerSerializer(marketer,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        user = User.objects.get(phoneNumber =request.data['phoneNumber'])
        marketer = Marketer.objects.get(user_id = user.id)
        serializer1 = serializers.MarketerSerializer(marketer)
        
        return Response(serializer1.data, status=status.HTTP_201_CREATED, headers=headers)