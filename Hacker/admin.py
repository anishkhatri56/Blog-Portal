from django.contrib import admin
from .models import  Room, Topic, Message,Blog






# Register your models here.
from .models import Project, Review, Tag




#Added for Trainer Room Message 
admin.site.register(Room)
admin.site.register(Topic)
admin.site.register(Message)


admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Tag)

admin.site.register(Blog)


