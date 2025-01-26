from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Conversation, Message, User

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Conversation)
