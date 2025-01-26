from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Conversation, Message, User


class UserAdmin(UserAdmin):
    fieldsets = (
        *UserAdmin.fieldsets,  # original form fieldsets, expanded
        (
            "Custom Field Heading",  # group heading of your choice; set to None for a blank space instead of a header
            {
                "fields": (
                    "phone_number",
                    "role",
                ),
            },
        ),
    )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Message)
admin.site.register(Conversation)
