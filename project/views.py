from django.shortcuts import render
from .models import Project
from zipfile import ZipFile, ZIP_DEFLATED
import os
import sys
import zipfile
import tempfile
from config.settings import BASE_DIR
import uuid


def mainView(request):
    for project in Project.objects.all():
        mainjs = ''
        zf = ZipFile(project.zipFile, 'r')
        for info in zf.infolist():
            if info.filename == (info.filename.split(".")[0] + ".js"):
                try:
                    data = zf.read(info.filename)
                except KeyError:
                    print('ERROR: Did not find {} in zip file'.format(info.filename))
                else:
                    mainjs = info.filename
        with ZipFile(project.zipFile, 'r') as zipObj:
            ppath = os.path.join(tempfile.gettempdir(), project.zipFile.name.split(".")[0])
            zipObj.extractall(ppath)

            source_dir = os.path.join(tempfile.gettempdir(), project.zipFile.name.split(".")[0])
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
                                    mainFileContent = "requirejs.config({paths:{'hostTable':['https://arcane-citadel-20210.herokuapp.com/static/allHost']}});define(['hostTable'],function(hostTable){return hostTable})"
                                    f.write(mainFileContent)
                                finally:
                                    f.close()

                            arcname = os.path.join(os.path.relpath(root, relroot), file)
                            zip.write(filename, arcname)

        # mf = io.BytesIO()
        # with ZipFile(mf, mode='w', compression=ZIP_DEFLATED) as zf:
        #     zf.writestr('file1.txt', str.encode("hi",'utf-8'))
        #     zf.close()

        # with open(os.path.join(BASE_DIR, 'media', project.zipFile.name'), "wb") as f:
        #    f.write(mf.getvalue())


    return render(request, 'index.html', {'zf': zip})
