from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views



urlpatterns = [
#for login 
path('login/', views.loginUser, name = 'login'),
path('logout/', views.logoutUser, name = 'logout'),
path('register-customer/', views.registerCustomer, name = 'register-customer'),
path('register-trainer/', views.registerTrainer, name = 'register-trainer'),
path ('contact/', views.contact, name = 'contact'),


path('profiles', views.profiles, name = "profiles"),
path ('user-profile/<str:pk>/', views.userProfile, name = "user-profile"),
path ('customer-profile/<str:pk>/', views.userProfile, name = "customer-profile"),
path('account/', views.userAccount, name = "account"),

path('edit-account/',views.editAccount, name = "edit-account"),
path('create-skill/',views.createSkill, name = "create-skill"),
path('create-skill/<str:pk>/',views.updateSkill, name = "update-skill"),
path('delete-skill/<str:pk>/',views.deleteSkill, name = "delete-skill"),  
path('inbox/', views.inbox, name = "inbox"),  
path('message/<str:pk>/', views.viewMessage, name = "message"),  
path ('create-message/<str:pk>/', views.createMessage, name = "create-message"),
]


