from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Review, Room
from django.forms import widgets
from django import forms 
from django.contrib.auth.models import User 


#this is for Trainer Room 
class RoomForm(ModelForm):
    class Meta:
        model =  Room
        fields = '__all__'
        exclude = ['host','participants']

class ProjectForm(ModelForm):
    class Meta:
        model =Project
        fields = ['title','featured_image','description',
        'demo_link','source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ReviewForm(ModelForm):
    class Meta:
        model = Review 
        fields = ['value','body']

    labels = {
        'value': 'Place your vote',
        'body': 'Add your coment with your vote'
    }
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args,**kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})


class UserForm(ModelForm):
    class Meta:
       model = User
       fields = ['username', 'email']

