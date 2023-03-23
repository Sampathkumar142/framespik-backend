from core.models import Avatar, Zone
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator,MinValueValidator
from django.db import models
from organization.models import Organization
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import random
import string

# ____________________________ Manage Users ______________________
class UserManager(BaseUserManager):

    def create_user(self,phoneNumber,password=None,is_staff=False,is_active=True,is_superuser=False,**extra_fields):
        if  not phoneNumber:
            raise ValueError('users must have a phone number')
        user_obj =self.model(
            phoneNumber =phoneNumber,
            **extra_fields
        )
        user_obj
        if password is not None:
            user_obj.set_password(password)
        user_obj.is_staff=is_staff
        user_obj.is_superuser = is_superuser
        user_obj.is_active =is_active
        user_obj
        user_obj.save(using=self._db)
        return user_obj


    def create_staffuser(self,phoneNumber,password=None,**extra_fields):
        user =self.create_user(
            phoneNumber,
            password=password,
            is_staff=True,
            **extra_fields
        )
        return user

    def create_superuser(self,phoneNumber,password=None,**extra_fields):
        user =self.create_user(
            phoneNumber,
            password=password,
            is_staff=True,
            is_superuser=True,
            **extra_fields
        )
        return user

class User(AbstractUser):
    avatar = models.ForeignKey(Avatar, on_delete=models.PROTECT,null =True,blank =True)
    dateOfBirth = models.DateField(blank=True, null=True)
    email = models.EmailField(
        unique=True, max_length=80, blank=True, null=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    first_name = None
    isAffiliate = models.BooleanField(default=False)
    isAppTourDone = models.BooleanField(default=False)
    isCustomer = models.BooleanField(default=False)
    isEmailVerified = models.BooleanField(default=False)
    isMarketEmployee = models.BooleanField(default=False)
    isOrganizationAdmin = models.BooleanField(default=False)
    isOrganizationStaff = models.BooleanField(default=False)
    isSoftwareTourDone = models.BooleanField(default=False)
    isWebTourDone = models.BooleanField(default=False)
    last_name = None
    name = models.CharField(max_length=25,null=True,blank =True)
    phoneNumber = models.CharField(unique=True, max_length=10,db_index=True)
    USERNAME_FIELD = "phoneNumber"
    username = None
    REQUIRED_FIELDS = []
    objects = UserManager()

    class Meta:
       indexes = [
           models.Index(fields=['phoneNumber'])
        ]

    def __str__(self) -> str:
        if self.name :
            return (self.name)
        return self.phoneNumber
    
    



# ___________________________ Organization (Proprietor, Employee)  Profile ________________________
class OrganizationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    whatsapp = models.CharField(max_length=10)



# ___________________________ Affiliate Profile __________________________
def generate_unique_string(length=6):
    while True:
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if not Affiliate.objects.filter(referCode=random_string).exists():
            return random_string


class Affiliate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    commissionPercentage = models.DecimalField(max_digits=4, decimal_places=2,default=settings.AFFILIATE_COMMISION_PERCENTAGE)
    joinedDate = models.DateField(auto_now_add=True)
    revenue = models.DecimalField(max_digits=9, decimal_places=2,null=True,blank=True,default=0)
    referCode = models.CharField(max_length=6,unique=True,default=generate_unique_string)


# ____________________________ Customer Profile ________________________
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ManyToManyField(Organization)
    # set Verify to True if OTP Verification Done
    isVerified = models.BooleanField(default=False)


# ____________________________ Customer login otp Stack ________________________
class customerOtpStack(models.Model):
    """
    customer OTP requests are stored here and when customer
    entered an OTP and submit we check from this stack and 
    is exist we create a customer or else we return JWT Token
    """
    phone_regex=phone_regex =RegexValidator(regex =r'^\+?1?\d{6,14}$',
        message="Phone number must be entered in the format:'+99999999'.Up to 14 digits allowed.")
    phoneNumber = models.CharField(validators=[phone_regex],max_length=10)
    otp = models.PositiveIntegerField()
    dateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.phoneNumber) +' is sent ' + str(self.otp)
# _________________________ Employee Roles Ex: manager, accountant, tel-caller _______________________
class EmployeeRole(models.Model):
    title = models.CharField(max_length=50)

    def __str__(self):
        return self.title


# _________________________ Employee Profile __________________________
class Employee(models.Model):
    address = models.CharField(max_length=255)
    interviewSummary = models.TextField()
    isManager = models.BooleanField()
    joinedDate = models.DateField(auto_now_add=True)
    phoneNumber = models.CharField(unique=True, max_length=10)
    role = models.ForeignKey(EmployeeRole, on_delete=models.PROTECT)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    aadharNumber = models.CharField(max_length=12, unique=True, validators=[
        RegexValidator(r'^[0-9]{12}$', 'Aadhar number must be 12 digits')
    ])
    panNumber = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', 'Invalid PAN number'),
        MinLengthValidator(10),
        MaxLengthValidator(10)
    ])
    bankAccountNumber = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(r'^[0-9]{9,18}$', 'Invalid bank account number'),
        MinLengthValidator(9),
        MaxLengthValidator(18)
    ])
    ifscCode = models.CharField(max_length=11, validators=[
        RegexValidator(r'^[A-Z]{4}[0-9]{7}$', 'Invalid IFSC code')
    ])
    nameAsPerBank = models.CharField(max_length=255)
    bankName = models.CharField(max_length=255)

    A_POS = 'A+'
    A_NEG = 'A-'
    B_POS = 'B+'
    B_NEG = 'B-'
    AB_POS = 'AB+'
    AB_NEG = 'AB-'
    O_POS = 'O+'
    O_NEG = 'O-'
    BLOOD_GROUP_CHOICES = [
        (A_POS, 'A+'),
        (A_NEG, 'A-'),
        (B_POS, 'B+'),
        (B_NEG, 'B-'),
        (AB_POS, 'AB+'),
        (AB_NEG, 'AB-'),
        (O_POS, 'O+'),
        (O_NEG, 'O-'),
    ]
    bloodGroup = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)


# _________________________ Marketing person Profile __________________________
class Marketer(models.Model):
    address = models.CharField(max_length=255)
    interviewSummary = models.TextField()
    isEligibleToTravel = models.BooleanField()
    isManager = models.BooleanField()
    joinedDate = models.DateField(auto_now_add=True)
    whatsapp = models.CharField(unique=True, max_length=10)
    salary = models.DecimalField(max_digits=9, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    zone = models.ManyToManyField(Zone)

    aadharNumber = models.CharField(max_length=12, unique=True, validators=[
        RegexValidator(r'^[0-9]{12}$', 'Aadhar number must be 12 digits')
    ])
    panNumber = models.CharField(max_length=10, unique=True, validators=[
        RegexValidator(r'^[A-Z]{5}[0-9]{4}[A-Z]{1}$', 'Invalid PAN number'),
        MinLengthValidator(10),
        MaxLengthValidator(10)
    ])
    bankAccountNumber = models.CharField(max_length=20, unique=True, validators=[
        RegexValidator(r'^[0-9]{9,18}$', 'Invalid bank account number'),
        MinLengthValidator(9),
        MaxLengthValidator(18)
    ])
    ifscCode = models.CharField(max_length=11, validators=[
        RegexValidator(r'^[A-Z]{4}[0-9]{7}$', 'Invalid IFSC code')
    ])
    nameAsPerBank = models.CharField(max_length=255)
    bankName = models.CharField(max_length=255)

    A_POS = 'A+'
    A_NEG = 'A-'
    B_POS = 'B+'
    B_NEG = 'B-'
    AB_POS = 'AB+'
    AB_NEG = 'AB-'
    O_POS = 'O+'
    O_NEG = 'O-'
    BLOOD_GROUP_CHOICES = [
        (A_POS, 'A+'),
        (A_NEG, 'A-'),
        (B_POS, 'B+'),
        (B_NEG, 'B-'),
        (AB_POS, 'AB+'),
        (AB_NEG, 'AB-'),
        (O_POS, 'O+'),
        (O_NEG, 'O-'),
    ]
    bloodGroup = models.CharField(
        max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)



class AdminPcloudCredential(models.Model):
    email = models.EmailField(max_length=225)
    password = models.CharField(max_length=225)
    lastLogin = models.DateField(null=True,blank=True)
    auth = models.CharField(max_length=400)
    
