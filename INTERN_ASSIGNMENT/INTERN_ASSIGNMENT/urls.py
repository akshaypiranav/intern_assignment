"""
INTERN - AKSHAY PIRANAV B
G-MAIL - akshaypiranavb@gmail.com
"""
from django.contrib import admin
from django.urls import path,include
 
from django.conf import settings
from django.conf.urls.static import static

#CREATED A URLS.PY AT THE APP SO WE INCLUDING IT
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('APP.urls')),
]
 
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)