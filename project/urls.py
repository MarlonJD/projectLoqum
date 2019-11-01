from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('project/<uuid:project_uuid>/', views.getKey, name='getKey'),
    path('getFile/<uuid:project_uuid>/<uuid:user_key>/.js', views.getFile, name='getFile')
]
