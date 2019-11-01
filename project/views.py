from django.shortcuts import render
from django.http import HttpResponse
from .models import Project, Key, RemoteFile
from zipfile import ZipFile, ZIP_DEFLATED
import os
import zipfile
import tempfile
import uuid
from django.core.mail import send_mail
import requests
import io


def index(request):
    return render(request, 'index.html', {'projects': Project.objects.all()})


def getFile(request, project_uuid, user_key):
    projectObj = Project.objects.get(unique_id=project_uuid)
    remoteFileObj = projectObj.remoteFile
    response = HttpResponse(content=remoteFileObj.content, content_type='application/javascript')
    response['Content-Disposition'] = 'attachment; filename="response.js"'
    return response


def getKey(request, project_uuid):
    '''
    Get Key View Function. User can take the key after register
    '''
    if request.method == 'POST':
        fullname = request.POST['name']
        company = request.POST['company']
        phone = request.POST['phone']
        email = request.POST['email']

        try:
            Key.objects.get(email=email)
        except Key.DoesNotExist:
            keyObj = Key(fullname=fullname,
                         company=company,
                         phone=phone,
                         email=email)
            keyObj.save()
        else:
            return render(request, 'alreadyGot.html')

        if request.method == 'POST':
            key = str(keyObj.uniqueKey)
            project = Project.objects.get(unique_id=project_uuid)

            mainjs = ''

            resFromUrl = requests.get(project.zipFile)
            resZip = io.BytesIO(resFromUrl.content)
            
            with ZipFile(resZip) as zf:
                for info in zf.infolist():
                    if info.filename == (info.filename.split(".")[0] + ".js"):
                        try:
                            data = zf.read(info.filename)
                        except KeyError:
                            print('ERROR: Did not find {} in zip file'.format(info.filename))
                        else:
                            mainjs = info.filename
                            print(mainjs)
            with ZipFile(resZip, 'r') as zipObj:
                ppath = os.path.join(tempfile.gettempdir(), mainjs.split("/")[0])
                zipObj.extractall(ppath)

                source_dir = os.path.join(tempfile.gettempdir(), mainjs.split("/")[0])
                relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
                with zipfile.ZipFile("media/" + str(uuid.uuid4())  + ".zip", "w", ZIP_DEFLATED) as zip:
                    for root, dirs, files in os.walk(source_dir):
                        zip.write(root, os.path.relpath(root, relroot))
                        for file in files:
                            filename = os.path.join(root, file)
                            if os.path.isfile(filename):
                                if mainjs in filename:
                                    print("Found: ", filename)
                                    try:
                                        f = open(filename, "w", encoding='utf-8')
                                        mainFileContent = 'requirejs.config({paths:{"loqum":["http://127.0.0.1/getFile/' + str(project.unique_id) + '/' + key + '/"]}});define(["loqum"],function(loqum){return loqum})'
                                        f.write(mainFileContent)
                                    finally:
                                        f.close()

                                arcname = os.path.join(os.path.relpath(root, relroot), file)
                                zip.write(filename, arcname)

                                send_mail(
                                    'Download Link is ready',
                                    'here is your download link http://asdfafda.com/' + zip.filename,
                                    'marylonjd@gmail.com',
                                    [keyObj.email],
                                    fail_silently=False,
                                )
        return render(request, 'getZip.html',
                      {'key': keyObj, 'zf': zip})
    else:
        project = Project.objects.get(unique_id=project_uuid)
        return render(request, 'getKey.html', {'project': project})
