from django.shortcuts import render
from .models import Project
import zipfile
import datetime
import os


def mainView(request):
    for project in Project.objects.all():
        zf = zipfile.ZipFile(project.zipFile, 'w')
        for info in zf.infolist():
            if info.filename == (info.filename.split(".")[0] + ".js"):
                try:
                    data = zf.read(info.filename)
                except KeyError:
                    print('ERROR: Did not find {} in zip file'.format(
                                                               filename))
                else:
                    print(info.filename, ':')

    return render(request, 'index.html', {'zf': zf})
