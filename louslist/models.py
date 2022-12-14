from django.db import models
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models import Avg
import requests
import json

from django import template

register = template.Library()

# Create your models here.


class Dept(models.Model):
    dept_name = models.CharField(max_length=50)
    dept_url_shorthand = models.CharField(max_length=15)

    def __str__(self):
        return self.dept_name


class Subject(models.Model):
    dept_name = models.ForeignKey(Dept, on_delete=models.CASCADE)
    mnemonic = models.CharField(max_length=5)
    subj_name = models.CharField(max_length=50)
    # rating = models.IntegerField(default=0)

    def __str__(self):
        return self.subj_name


class Search(models.Model):
    mnemonic = models.CharField(max_length=4)
    course_num = models.CharField(max_length=4)

    def form_valid(self, form):
        form.save()
        return redirect(reverse('search-results'))

    def __str__(self):
        return self.course_num


class FriendRequest(models.Model):
    from_user = models.ForeignKey(
        User, related_name="from_user", on_delete=models.CASCADE)
    to_user = models.ForeignKey(
        User, related_name="to_user", on_delete=models.CASCADE)

    @register.filter
    def getUsername(self):
        return self.to_user.username

    def __str__(self):
        return self.from_user.first_name + " " + self.from_user.last_name + " wants to be friends"


class CourseModel(models.Model):
    course_num = models.CharField(max_length=5, primary_key=True)
    course = models.CharField(max_length=20)
    name = models.CharField(max_length=50)
    instructor = models.CharField(max_length=50)
    meeting_days = models.CharField(max_length=10)
    meeting_time = models.CharField(max_length=10)
    location = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.course + "with" + self.instructor + "on" + self.meeting_days + "at" + self.


class Friendship(models.Model):
    person1 = models.ForeignKey(
        User, related_name="person1", on_delete=models.CASCADE)
    person2 = models.ForeignKey(
        User, related_name="person2", on_delete=models.CASCADE)

    def __str__(self):
        return self.person2.username
    # def __str__(self):
    #     return f"User #{self.person1} is friends with #{self.person2}"

    # def __str__(self):
    #     return self.course + "with" + self.instructor + "on" + self.meeting_days + "at" + self.meeting_time


class CourseRating(models.Model):
    course_num = models.CharField(max_length=6)

    def average_rating(self):
        return Rating.objects.filter(course=self).aggregate(Avg('rating'))['rating__avg'] or 0.0

    def __str__(self):
        return f"{self.average_rating()}"


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseRating, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['user', 'course'], name='user_rates_once_per_course')]


class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    

    def get_query_set(self):
        return Event.objects.filter(schedule=self)
    
    def __str__(self):
        return f"{self.user.first_name}'s Schedule"


class Event(models.Model):
    course = models.JSONField()
    course_num = models.IntegerField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

class CommentText(models.Model):
    schedule = models.ForeignKey(Schedule, related_name="comments", on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    publish_date = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return 'Comment {} by {}'.format(self.text,self.user.username)
