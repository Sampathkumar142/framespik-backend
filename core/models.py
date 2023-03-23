from django.db import models

# ____________________________ INDIA States ______________________
class State(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# ____________________________ Manage Organization Zones (subset of States) Ex: Rajahmundry, Kakinada, Vizag ______________________
class Zone(models.Model):
    state = models.ForeignKey(State, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title


# ___________________________ Cities ________________________________
class Place(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.PROTECT)
    name = models.CharField(max_length=50)


# ___________________________ Avatars _____________________________
class Avatar(models.Model):
    thumb = models.URLField(unique=True)
    pcloudImageID = models.CharField(max_length=100)
    pcloudPublicCode = models.CharField(max_length=1000)

    MALE = 'M'
    FEMALE = 'F'
    OTHER = 'O'
    GENDER_CHOICE = {
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (OTHER, 'Other'),
    }
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)


# ____________________________ Transaction Modes Ex: Cash, Cheque, Bank-Transfer, Phonepe, Gpay _____________________
class TransactionMode(models.Model):
    name = models.CharField(max_length=40)


# ____________________________ Music _________________________________
class Music(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField()
