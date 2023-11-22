from multiprocessing import context
import profile 
from pydoc_data.topics import topics
from telnetlib import AUTHENTICATION
from urllib import request
from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.urls import reverse
from .models import Message, Room
from .forms import RoomForm, ProjectForm, ReviewForm, UserForm
from .models import Topic 
from .models import Blog
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Tag
from django.contrib import admin
from .utils import searchProjects,paginateProjects
from django.db.models import Q
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group
from django.contrib.auth import logout, authenticate, login

from users.models import Contact
from users.models import Profile
from users.forms import CustomUserCreationForm

# for inbox message
from users.forms import CustomUserCreationForm, ProfileForm, SkillForm, InboxMessageForm


def index(request):
    data = Blog.objects.all()
    return render(request, 'index.html',{"blogs":data})

def single(request,slug):
    data = Blog.objects.get(slug=slug)
    return render(request, 'single.html',{"blog":data})
    



    
# Messaging communication in our website 
# @login_required(login_url='login')
@login_required(login_url = 'login')
def communicate(request):
    #Query for room database 
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__contains = q) |
        Q(name__contains=q)  |
        Q(description__contains=q)
    )
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context ={'rooms':rooms, 'topics':topics,
    'room_count': room_count, 'room_messages': room_messages }
    return render( request, 'communicate.html', context)




# @login_required(login_url='login')
#Primary key added to distinguish between the rooms. 
def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all().order_by('-created')
    patricipants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
        user=request.user,
        room=room,
        body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect ('room', pk = room.id)

    context = {'room': room, 'room_messages': room_messages, 'participants':patricipants }
    return render( request, 'room.html', context )




def customerProfile(request,pk):
    profile = Profile.objects.get(id = pk)
    topSkills = profile.skill_set.exclude(description__exact = "")
    otherSkills = profile.skill_set.filter(description = "")
    context = {'profile': profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render (request, 'users/user-profile.html', context )





@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)

        Room.objects.create(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description =request.POST.get('description'),
        )
        return redirect('communicate')

    context = {'form':form, 'topics':topics}
    return render(request, 'room_form.html',context)





@login_required(login_url='login')
def updateRoom(request,pk):
    topics = Topic.objects.all()
    room = Room.objects.get(id=pk)
    form = RoomForm(request.POST,request.FILES, instance=room)

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name = topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('communicate')

    context = {'form':form, 'topics':topics, 'room':room}
    return render(request, 'room_form.html',context)





@login_required(login_url='login')
def deleteRoom(request,pk):
    room = Room.objects.get (id=pk)
    context = {'room':room}
    if request.method == 'POST':
        room.delete()
        return redirect('communicate')
    return render(request, 'delete_template.html',context )





@login_required(login_url='login')
def deleteMessage(request,pk):
    message = Message.objects.get (id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed to this room')

    if request.method == 'POST':
        message.delete()
        return redirect('communicate')
    return render(request, 'delete_template.html',{'obj':message} )






def projects(request):  
   projects, search_query = searchProjects(request)
   custom_range, projects = paginateProjects(request,projects,3)

   context = {'projects':projects, 'search_query':search_query,  'custom_range':custom_range}
   return render (request, 'projects.html', context)







def project(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit = False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        # update  project vote count 
        messages.success(request, 'Your review was sucessfully submitted')
        return redirect('project' ,pk = projectObj.id)
    return render (request, 'single.project.html', {'project': projectObj,'form':form})

def Vlog(request,pk):
    projectObj = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        review = form.save(commit = False)
        review.project = projectObj
        review.owner = request.user.profile
        review.save()

        projectObj.getVoteCount

        # update  project vote count 
        messages.success(request, 'Your review was sucessfully submitted')
        return redirect('project' ,pk = projectObj.id)
    return render (request, 'single.project.html', {'project': projectObj,'form':form})






    
@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit = False)
            project.owner = profile
            project.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name = tag )
                project.tags.add(tag)
            return redirect('account')
    context = {'form':form}
    return render(request, "project_form.html", context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def updateProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance = project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace(','," ").split()

        form = ProjectForm(request.POST, request.FILES, instance = project )
        if form.is_valid():
            project = form.save()
            for tag in newtags:
                tag, created = Tag.objects.get_or_create(name = tag )
                project.tags.add(tag)
            return redirect('account')
    context = {'form':form, 'project':project}
    return render(request, "project_form.html", context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','trainer'])
def deleteProject(request,pk):
    profile = request.user.profile
    project = profile.project_set.get (id = pk)
    if request.method == 'POST':
        project.delete()
        return redirect(projects)

    context = {'object': project }
    return render(request, 'delete_template.html', context)





@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance = user)
    context = {'form': form}


    if request.method == 'POST':
        form = UserForm(request.POST, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
    return render (request, 'update_user.html', context)




# def loginCustomer(request):
#     group = None
#     page = 'login'

#     if request.method == 'POST':
#             useraccountname = request.POST['username']
#             password = request.POST['password']
        
#             try: 
#               user = User.objects.get(username=useraccountname)

#             except:
                
#                messages.error(request, 'User does not exist')
            
#             user = authenticate(request, username=useraccountname, password=password)

#             if user is not None:
#                 login(request, user)
#                 return redirect(request, 'project-customer')
#                 # GET['next'] if 'next' in request.GET else
            
#             if request.user.groups.exists():
#                 group = request.user.groups.all()[0].name

#             else:
#                 messages.error(request, 'username or password is incorrect!! ')
#     return render(request, 'login_customer.html')



# def registerCustomer(request):
#     page = 'register'
#     form = CustomUserCreationForm()

#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.username = user.username.lower()
#             user.save()

#             group = Group.objects.get(name='trainer')
#             user.groups.add(group)

#             messages.success(request, 'User account is created! thank you ')

#             login(request,user)
#             return redirect('communicate')

#         else:
#             messages.success(request,'An error has occured during registration.')
#     context = {'page': page, 'form':form }
#     return render (request, 'login_customer.html', context )






## for mobile flexible desing, browse topics and Recent Activity 
def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    context = {'topics':topics}
    return render(request, 'topics.html', context )





#Activity in small screen devices 
def activityPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages': room_messages}
    return render(request, 'activity.html', context )
    
    


## for footer design and content 
@login_required(login_url='login')
def AboutUs(request):
    return render(request, 'about.html')


 # for membership of the program 
@login_required(login_url='login')
def userMembership(request):
    context = {}
    return render(request, 'membership.html', context)

@login_required(login_url='login')
def userCheckout(request):
    context = {}
    return render(request, 'checkout.html', context)

@login_required(login_url='login')
def joinVideo(request):
    context = {}
    return render(request,'agora.html', context)




# for customer rendering 
def projectsCustomer(request):  
   projects, search_query = searchProjects(request)
   custom_range, projects = paginateProjects(request,projects,3)

   context = {'projects':projects, 'search_query':search_query,  'custom_range':custom_range}
   return render (request, 'projects_customer.html', context)


# for inbox message
@login_required(login_url = 'login')
def viewMessage(request,pk):
    profile = request.user.profile
    message = profile.messages.get(id=pk)
    if message.is_read == False:
        message.is_read = True
        message.save()
    context = {'message':message}
    return render(request, 'users/message.html', context)


def createMessage(request,pk):
    recipient = Profile.objects.get(id=pk)
    form = InboxMessageForm()

    try:
        sender = request.user.profile
    except:
        sender = None

    if request.method == 'POST':
        form = InboxMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request,'Your message was sucessfully sent')
            return redirect('user-profile',pk=recipient.id)


    context = {'recipient':recipient, 'form':form}
    return render(request, 'users/message_form.html',context)


def home_contact(request):
    if request.method == "POST" :
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc= request.POST.get('desc')
        contact = Contact (name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!.')
        return redirect('home_contact')
    return render (request,'home_contact.html' )



def contact(request):
    if request.method == "POST" :
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc= request.POST.get('desc')
        contact = Contact (name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!.')
        return redirect('home_contact')
    return render (request,'contact.html' )


