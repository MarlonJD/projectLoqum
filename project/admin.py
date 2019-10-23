from django.contrib import admin
from .models import Project ,RemoteFile
from django import forms


class MyModelForm(forms.ModelForm):
    MY_CHOICES = (
        ('js', 'Javascript'),
        ('css', 'CSS'),
    )

    fileType = forms.ChoiceField(choices=MY_CHOICES)

class MyModelAdmin(admin.ModelAdmin):
    fields = ('name', 'fileType', 'version', 'content')
    list_display = ('fileType', )
    form = MyModelForm

admin.site.register(RemoteFile, MyModelAdmin)
admin.site.register(Project)
