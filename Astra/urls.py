"""Astra URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include 
from django.conf import settings
from django.conf.urls.static import static


from django.contrib.auth import views as auth_views


from Astra.settings import MEDIA_ROOT
from Astra.settings import STATIC_ROOT

admin.site.site_header = "TrainerRoom ADMIN "
admin.site.site_title = "ADMIN PORTAL"
admin.site.index_title = "Welcome ADMIN portal of TrainerRooms"



app_name = 'Hacker'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Hacker.urls')),
    path('',include('users.urls')),
    path('Products/', include('Products.urls')),
    # path('Payment_Handler/', include('Payment_Handler.urls')),
    # path('Video_Chat/', include('Video_Chat.urls')),
    path('api/',include('api.urls')),


    path('reset_password/', auth_views.PasswordResetView.as_view(template_name ="reset_password.html"),
    name = "reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = "reset_password_sent.html"),
    name = "password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "reset.html"),
    name = "password_reset_confirm"),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = "reset_password_complete.html"),
    name = "passsword_reset_complete"),
   
 

]

urlpatterns += static(settings.MEDIA_URL, document_root = MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root = STATIC_ROOT)