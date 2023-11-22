from email.policy import default

from django.db import models
from django.contrib.auth.models import User
import uuid
from users.models import Profile 
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

# Create your models here
    
# class User(AbstractUser):
#     is_admin = models.BooleanField("Is admin", default = False)
#     is_Customer = models.BooleanField('Is customer', default = False)
#     is_trainer = models. BooleanField('Is trainer', default = False )

 

class Topic(models.Model):
    name = models.CharField(max_length = 200)

    def __str__(self):
         return self.name
    

class Room(models.Model):
    host = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    topic = models.ForeignKey(Topic, on_delete = models.SET_NULL, null = True)
    name = models.CharField(max_length = 200)
    description = models.TextField(null = True, blank = True)
    participants = models.ManyToManyField(User, related_name = 'participants', blank = True )
    updated = models.DateTimeField(auto_now = True)
    created = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.name
    
    class Meta:
       ordering = ['-updated', '-created']







class Message(models.Model):
    #default user by django source: https://docs.djangoproject.com/en/4.0/ref/contrib/auth/
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    #1 to many relationship (1:M)
    #room = models.ForeignKey(Room, on_delete = models.SET_NUll) (this will make the romm null but the data will still be in the databse)
    room = models.ForeignKey(Room, on_delete = models.CASCADE, null = True ) #Will delete all the data
    body = models.TextField(null = True )
    updated = models.DateTimeField(auto_now = True, null = True )
    created = models.DateTimeField(auto_now_add = True, null = True )


    class Meta:
       ordering = ['-updated', '-created']
   
    # def __str__ (self):
    #      return self.body[0:50]

class Project(models.Model):
    owner = models.ForeignKey(Profile, null = True, blank = True, on_delete = models.SET_NULL)
    title = models.CharField(max_length=200)
    description = models.TextField(null = True, blank = True)
    demo_link = models.CharField(max_length = 2000, null = True, blank = True)
    featured_image = models.ImageField(null = True, blank = True, default = "default.jpg")
    source_link = models.CharField(max_length =2000, null = True, blank = True)
    tags = models.ManyToManyField('Tag', blank = True)
    vote_total = models.IntegerField(default = 0, null = True, blank = True)
    vote_ratio = models.IntegerField(default = 0, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__ (self):
        return self.title

    class Meta: 
        ordering = ['-vote_ratio', '-vote_total', 'title']

    @property
    def imageURL(self):
        try:
            url = self.featured_image.url
        except:
            url = ''
        return url

        
    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat = True)
        return queryset

    
    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value = 'up').count()
        totalVotes = reviews.count()

        ratio = (upVotes / totalVotes ) * 100
        self.vote_total  = totalVotes
        self.vote_ratio = ratio 

        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'Up Vote'),
        ('down', 'Down Vote'),
    )
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    body = models.TextField(null = True, blank = True)
    value = models.CharField(max_length=200, choices = VOTE_TYPE)
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)

    class Meta: 
        unique_together = [['owner','project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name = models.CharField(max_length = 200 )
    created = models.DateTimeField(auto_now_add = True)
    id = models.UUIDField(default = uuid.uuid4, unique=True, primary_key = True, editable=False)

    def __str__(self):
        return self.name




class Blog(models.Model):
    title = models.CharField(max_length = 155)
    content = models.TextField()
    slug = models.SlugField(max_length = 255)
    featured_image = models.ImageField(upload_to= "img/Blog")

    def __str__(self):
        return self.title