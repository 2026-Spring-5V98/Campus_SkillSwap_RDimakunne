from django.contrib import admin
from .models import Skill, Review, Appointment, Notification


# @admin.register is a cleaner alternative to admin.site.register(Skill, SkillAdmin)
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # Columns shown in the admin list view
    list_display = ['title', 'owner', 'category', 'is_free', 'price', 'availability_status', 'created_at']

    # Sidebar filters on the right side of the admin list
    list_filter = ['category', 'availability_status', 'is_free']

    # Makes the search box work on these fields
    search_fields = ['title', 'description', 'owner__username']


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['requester', 'skill', 'date', 'time', 'status', 'created_at']
    list_filter = ['status']
    search_fields = ['requester__username', 'skill__title']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'message', 'is_read', 'created_at']
    list_filter = ['is_read']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'reviewee', 'rating', 'created_at']
    list_filter = ['rating']
    search_fields = ['reviewer__username', 'reviewee__username']
