from utilitys.pCloud import BASE_URL,headers,endSession,login
import requests
from .models import OrganizationPcloudCredentials
import datetime

def loginAdmin(organization_id):
    try:
        account = OrganizationPcloudCredentials.objects.get(organization_id = organization_id)
    except OrganizationPcloudCredentials.DoesNotExist:
        account = None
    if account:
        today = datetime.now().date()
        diff = (today - account.lastUpdate).days
        if diff > 20:
            response = login(account.email, account.password)
            if response != 400:
                endSession(account.auth)
                account.auth = response
                account.save()
                return response
            else:
                return None
        else:
            return account.auth
    return None


def register(email,password):
    response = requests.get(
        f"{BASE_URL}/register?termsaccepted=yes&mail={email}&password={password}&os=4&device=Mozilla%2F5.0+(Windows+NT+10.0%3B+Win64%3B+x64)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F111.0.0.0+Safari%2F537.36&language=en&ref=87070"
                            )
    response = response.json()
    print(response)
    if response['result'] == 0:
        return 200
    return 400



def getAuth(organization_id):
    try:
        account = OrganizationPcloudCredentials.objects.get(organization_id = organization_id)
    except OrganizationPcloudCredentials.DoesNotExist:
        account = None
    if account:
        today = datetime.datetime.now().date()
        if account.lastLogin is not  None:
            diff = (today - account.lastLogin).days
        else:
            diff = 200
        if diff > 20:
            response = login(account.email, account.password)
            if response != 400:
                endSession(account.auth)
                account.auth = response
                account.lastLogin = today
                account.save()
                return response
            else:
                return None
        else:
            return account.auth
    return None


