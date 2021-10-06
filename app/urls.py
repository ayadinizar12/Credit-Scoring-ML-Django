

from django.urls import path, re_path
from app import views
from . import views_dash

from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [

    # The home page
    

    path('', views.index, name='home'),
    path('result/', views_dash.result, name='result'),
    path('upload/',views.upload,name = 'upload'),
    path('result_pdf/',views.result_pdf,name = 'result_pdf'),

    
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),
    

]

if settings.DEBUG:
    urlpatterns += static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

