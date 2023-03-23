import requests


BASE_URL = 'https://eapi.pcloud.com'

# to just pass the request as sending from the browser window
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
}


# return auth token on successful login else return -> ERRORCODE - ERRORTEXT
def login(email, password):
    response = requests.get(
        f'{BASE_URL}/userinfo?getauth=1&username={email}&password={password}', headers=headers)
    response = response.json()
    if (response['result'] != 0):
        return 400
    auth = response['auth']
    return auth


# get account info without login or generating new token
def getAccountInfo(email, password):
    response = requests.get(
        f'{BASE_URL}/userinfo?username={email}&password={password}', headers=headers)
    response = response.json()
    if (response['result'] != 0):
        return f'{response["result"]} - {response["error"]}'
    return response


# expire the token which is passed and return 200 success || else return 400 if failed
def endSession(auth):
    response = requests.get(f'{BASE_URL}/logout?auth={auth}', headers=headers)
    response = response.json()
    if (response['auth_deleted'] == True):
        return 200
    return 400


# Create folder at given path and name and return folder id
def createFolder(auth, path, name):
    response = requests.post(
        f'{BASE_URL}/createfolderifnotexists?auth={auth}&path=/{path}{name}')
    response = response.json()
    if (response['result'] == 0):
        folderId = response['metadata']['folderid']
        return folderId
    return 400


# Delete entire folder of the given folder id
def deleteFolder(auth, folderid):
    response = requests.post(
        f'{BASE_URL}/deletefolderrecursive?auth={auth}&folderid={folderid}')
    response = response.json()
    if response['result'] == 0:
        return 200
    return 400


# Delete file of the given file id
def deleteFile(auth, fileid):
    response = requests.post(
        f'{BASE_URL}/deletefile?auth={auth}&fileid={fileid}')
    response = response.json()
    if response['result'] == 0 or response['result'] == 2009:
        return 200
    return 400


# upload file to the given path or folderID
def uploadFile(auth, data, folderPath=None, folderid=None):
    file = {'file': data}
    if folderid:
        response = requests.post(
            f'{BASE_URL}/uploadfile?auth={auth}&folderid={folderid}&nopartial=1&renameifexists=1&filename=rcstudio', files=file)
    elif folderPath:
        response = requests.post(
            f'{BASE_URL}/uploadfile?auth={auth}&path={folderPath}&nopartial=1&renameifexists=1&filename=rcstudio', files=file)
    response = response.json()
    print(response['result'])
    if response['result'] == 0:
        fileId = response['fileids'][0]
        pubLinkResponse = getPublicLinkCode(auth, fileId)
        if pubLinkResponse != 400:
            code = pubLinkResponse
            link = f'{BASE_URL}/getpubthumb?code={code}&size=2048x2048'
            return {'fileid': fileId, 'publiclink': link, 'code': code}
    return 400


# return public link code of the file and can use for getting thumbnail
def getPublicLinkCode(auth, fileid):
    response = requests.post(
        url=f'{BASE_URL}/getfilepublink?auth={auth}&fileid={fileid}')
    response = response.json()
    if response['result'] == 0:
        return response['code']
    return 400


def getPubSmallThumb(code, size):
    return f'{BASE_URL}/getpubthumb?code={code}&size={f"{size}x{size}"}'


# return all file id's in the given folder Id as list
def getItemsInFolder(auth, folderid=None,path=None):
    if path is not None:
        response = requests.post(
        f'{BASE_URL}/listfolder?auth={auth}&path={path}')
    else:
        response = requests.post(
            f'{BASE_URL}/listfolder?auth={auth}&folderid={folderid}')
    response = response.json()
    if response['result'] == 0:
        # return [element['fileid'] for element in response['metadata']['contents'] if element.get('fileid') != None]
        return response
    return 400
