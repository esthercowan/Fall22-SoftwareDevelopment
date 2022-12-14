from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Dept, Subject, CourseRating, Rating, Schedule, Event, CommentText
# Register your models here.

class DeptAdmin(admin.ModelAdmin):
    fields = ['dept_name', 'dept_url_shorthand']
    
class SubjectAdmin(admin.ModelAdmin):
    fields = ['dept_name', 'mnemonic', 'subj_name']

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'schedule', 'text', 'publish_date')
    list_filter = ('publish_date')
    search_fields = ('user', 'text')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    
    
    
admin.site.register(Dept, DeptAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Rating)
admin.site.register(CourseRating)
admin.site.register(Schedule)
admin.site.register(Event)
admin.site.register(CommentText)
