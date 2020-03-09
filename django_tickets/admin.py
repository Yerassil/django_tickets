from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Ticket, Approval


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username']


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        'author', 'title', 'date_created'
    ]


@admin.register(Approval)
class ApprovalAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'ticket', 'approved'
    ]
