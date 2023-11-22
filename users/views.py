import contextlib
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from .models import Profile, InboxMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, InboxMessageForm
from django.db.models import Q
from .utils import searchProfiles,paginateProfiles
from .models import Contact
from datetime import datetime
from Hacker.decorators import unauthenticated_user,allowed_users,admin_only

from django.contrib.auth.models import Group
from Hacker.views import customerProfile

# Create your views here.

# @allowed_users(allowed_roles=['trainer'])
# @admin_only
def loginUser(request):
    group = None
    page = 'login'

    if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
        
            try: 
              user = User.objects.get(username=username)

            except:
                
               messages.error(request, 'User does not exist')
            
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect(request.GET['next'] if 'next' in request.GET else 'edit-account')
            
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            else:
                messages.error(request, 'username or password is incorrect!! ')
    return render(request, 'login_customer.html')



def logoutUser(request):
    logout(request)
    messages.info(request, 'User sucessfully loged out  ')
    return redirect('index')


def registerCustomer(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            

            group = Group.objects.get(name='Member')
            user.groups.add(group)

            messages.success(request, 'User account is created! Please sign In! ')

            login(request,user)
            return redirect('login')

        else:
            messages.success(request,'Please try password as combination of letters and numbers, and not relavent to your name and email.')
    context = {'page': page, 'form':form }
    return render (request, 'users/register_customer.html', context )
        
def registerTrainer(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            

            group = Group.objects.get(name='Player')
            user.groups.add(group)

            messages.success(request, 'User account is created! Please sign In! ')

            login(request,user)
            return redirect('login')

        else:
            messages.success(request,'Please try password as combination of letters and numbers, and not relavent to your name and email')




    context = {'page': page, 'form':form }
    return render (request, 'users/register_trainer.html', context )



# @login_required(login_url='login')

def profiles(request):
    profiles, search_query = searchProfiles(request)

    custom_range, profiles = paginateProfiles(request, profiles,6)
    
    context = {'profiles': profiles , 'search_query':search_query,'custom_range':custom_range}
    return render( request, 'users/profiles.html', context )

# @login_required(login_url='login')


def userProfile(request,pk):
    profile = Profile.objects.get(id = pk)
    topSkills = profile.skill_set.exclude(description__exact = "")
    otherSkills = profile.skill_set.filter(description = "")
    context = {'profile': profile, 'topSkills':topSkills, 'otherSkills':otherSkills}
    return render (request, 'users/user-profile.html', context )

def customerProfile(request,pk):
    profile = Profile.objects.get(id = pk)
    context = {'profile': profile}
    return render (request, 'users/customer-profile.html', context )

@login_required(login_url = 'login')
def userAccount(request):
    profile = request.user.profile

    skills = profile.skill_set.all()
    projects = profile.project_set.all()


    context = {'profile':profile, 'skills':skills, 'projects':projects}
    return render(request, 'account.html', context)

@login_required(login_url = 'login')
def editAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance = profile)
        if form.is_valid():
            form.save()
            return redirect('account')
    context = {'form':form}
    return render (request, 'users/profile_form.html', context)

@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin','trainer'])
def createSkill(request):
    profile = request.user.profile 
    form = SkillForm()

    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit = False)
            skill.owner = profile
            skill.save()
            messages.success(request,'New skill added sucessfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/skill_form.html', context )


@login_required(login_url = 'login')
@allowed_users(allowed_roles=['admin','trainer'])
def updateSkill(request, pk):
    profile = request.user.profile 
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if request.method =='POST':
        form = SkillForm(request.POST, instance= skill)
        if form.is_valid():
            skill.save()
            messages.success(request,'New skill updated sucessfully')
            return redirect('account')
    context = {'form':form}
    return render(request, 'users/skill_form.html', context )

@allowed_users(allowed_roles=['admin','trainer'])
def deleteSkill(request,pk):
    profile = request.user.profile
    skill = profile.skill_set.get (id = pk)
    if request.method == 'POST':
        skill.delete()
        return redirect('account')
        
    context = {'object': skill }
    return render(request, 'delete_template.html', context)

@login_required(login_url='login')
def contact(request):
    if request.method == "POST" :
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc= request.POST.get('desc')
        contact = Contact (name=name, email=email, phone=phone, desc=desc, date=datetime.today())
        contact.save()
        messages.success(request, 'Your message has been sent!.')
        return redirect('contact')
    return render (request,'contact.html' )

@login_required(login_url = 'login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()
    unreadCount = messageRequest.filter(is_read  = False).count()
    context = {'messageRequest': messageRequest, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html',context )

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



