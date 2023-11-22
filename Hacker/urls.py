from django.contrib import admin
from django.urls import path
from . import views
# for password reset
from django.contrib.auth import views as auth_views

from django.conf import settings 
from django.conf.urls.static import static

# app_name="Astra"

urlpatterns = [   
    # Added 
    # path('', views.index, name = 'index'),
    path('projects', views.projects, name = 'projects'),
    path('project-obj/<str:pk>/', views.project, name = 'project'),
    path('create-project/', views.createProject, name = 'create-project'),
    path('update-project/<str:pk>/', views.updateProject, name = 'update-project'),
    path('delete-project/<str:pk>/', views.deleteProject, name = 'delete-project'),
    path('vlogs', views.Vlog, name = 'vlogs'),

    






    # Added later for Trainer Room 
    path('', views.index, name = 'index'),
    path('communicate/', views.communicate, name = 'communicate'),
    path('room/<str:pk>/', views.room, name = 'room'),
    path('customer-profile/<str:pk>/', views.customerProfile, name ='customer-profile'),
    # path ('profile/<str:pk>/', views.userProfile, name = "user-profile"),
    
    path('create-room/', views.createRoom, name = "create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name = "update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name = "delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name = "delete-message"),

    path('update-user', views.updateUser, name = "update-user"),
    # path('login/', views.loginCustomer, name = 'login'),
    # path('register-customer/', views.registerCustomer, name = 'register-customer'),
    ## for flexible device design 
    path('topics/', views.topicsPage, name = 'topics'),
    path('activity/', views.activityPage, name = 'activity'),


    ## this is for footer 
    path('about/', views.AboutUs, name = 'about'),
    path('video/', views.joinVideo, name = 'video'),
    
    # for membership of the program 
    path('membership/', views.userMembership, name = 'membership'),
    path('checkout/', views.userCheckout, name = 'checkout'),

    # for customer rendering 
    path('project-customer', views.projectsCustomer, name = 'project-customer'),

    # for inbox
    # path ('create-message/', views.createMessage, name = "create-message"),

    # from home contact page pop-up 
    path ('home_contact/', views.home_contact, name = 'home_contact'),

    path ('contact/', views.contact, name = 'contact'),
    

    # for viewing the blog 
    path ('single/<slug:slug>', views.single, name="singel"),
]


