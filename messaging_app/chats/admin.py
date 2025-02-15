from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Conversation, Message, User


class UserAdmin(UserAdmin):
    readonly_fields = ("created_at", "user_id")
    fieldsets = (
        *UserAdmin.fieldsets,
        (
            "Custom Field Heading",
            {
                "fields": (
                    "user_id",
                    "phone_number",
                    "role",
                    "created_at",
                    "password_hash",
                ),
            },
        ),
    )


class MessageAdmin(admin.ModelAdmin):
    list_display = ("message_body", "sender", "conversation", "sent_at")
    search_fields = ("message_body", "sender__username")
    list_filter = ("sender", "conversation")
    readonly_fields = ("sent_at", "message_id")
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("message_id", "sender", "message_body", "conversation"),
            },
        ),
        ("Timestamps", {"fields": ("sent_at",)}),
    )


class ConversationAdmin(admin.ModelAdmin):
    list_display = ("conversation_owner", "created_at")
    search_fields = ("conversation_owner__username",)
    list_filter = ("conversation_owner",)
    readonly_fields = ("created_at",)
    fieldsets = (
        (
            "Basic Information",
            {
                "fields": ("conversation_owner", "participants"),
            },
        ),
        ("Timestamps", {"fields": ("created_at",)}),
    )


# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Conversation, ConversationAdmin)
