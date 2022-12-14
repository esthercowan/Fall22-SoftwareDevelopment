from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django import forms
from .forms import SearchForm, CommentForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta
# Create your views here.
import json
import requests

from .models import Dept, Search, FriendRequest, Friendship, CourseRating, Rating, Schedule, Event, CommentText



def login(request):
    return render(request, 'login.html')


def logout(request):
    return render(request, 'login.html')


def homeView(request):
    return render(request, "home.html")


def scheduleView(request):
    sched, created = Schedule.objects.get_or_create(user=request.user)
    comment_list = []
    class_times = dict()  
    flag = 1
    sched = Schedule.objects.filter(user=request.user)
    event_list = list(Event.objects.filter(schedule__in=sched))
    course_list = []
    for event in event_list:
        course_list.append(event.course)
    for course in course_list:
        # looks like 'meetings': [{'days': 'MoWeFr', 'start_time': '10.00.00.000000-05:00', 'end_time': '10.50.00.000000-05:00', 'facility_description': 'Rice Hall 340'}]
        
        class_name = course['subject'] + " " + course['catalog_number']
        times = course['meetings'][0]
        if times['start_time'] == '':
            continue
        start_time = datetime.strptime(times['start_time'][:5], '%H.%M')
        end_time = datetime.strptime(times['end_time'][:5], '%H.%M')
        # turn into blocks
        diff = timedelta(minutes=30)
        blocks = []
        time_ptr = start_time
        while time_ptr < end_time:
            blocks.append(datetime.strftime(time_ptr, "%I:%M %p"))
            time_ptr += diff
        days = parse_days(times['days'], flag)
        class_times[class_name] = [blocks, days]
        flag += 1
        
    
    time_blocks = dict()
    format = '%H:%M'
    for hour in range(8, 21):
        for minute in range(0, 60, 30):
            time_blocks[datetime.strftime(datetime.strptime('{:02d}:{:02d}'.format(hour, minute), format), "%I:%M %p")] = [0 for i in range(5)]
    # want dict with key = time and value = list of len 5 representing days
    # change values of days for each class to highlight the right days
    for c in class_times:
        first = True
        for block in class_times[c][0]:
            if first:
                """print(block)
                print(time_blocks[block])
                print(class_times[c][1])"""
                time_blocks[block] = [c if class_times[c][1][x] != 0 else time_blocks[block][x] if time_blocks[block][x] != 0 else 0 for x in range(5)]
                """print(time_blocks[block])
                print()"""
                first = False
            else:
                # 23 is arbitrary number for conflict error
                """print(block)
                print(time_blocks[block])
                print(class_times[c][1])"""
                time_blocks[block] = [x[0] if (isinstance(x[0], str) and x[1] == 0) else 23 if (isinstance(x[0], str) and x[1] != 0) or (x[0] != 0 and x[1]) else x[0]+x[1] for x in zip(time_blocks[block], class_times[c][1])] # add list marking days from course to current days 
                """
                print(time_blocks[block])
                print()
                """
    model = CommentText
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.schedule = sched[0]
            comment.save()  
            form = CommentForm()
            comments = list(CommentText.objects.filter(schedule__in=sched))
            context = {"time_blocks": time_blocks, "courses": course_list, "form": form, "comments": comments}
            return render(request, "proto_schedule.html", context=context)
    else:   
        form = CommentForm(request.POST)
        comments = list(CommentText.objects.filter(schedule__in=sched))
        context = {"time_blocks": time_blocks, "courses": course_list, "form": form, "comments": comments}
        return render(request, "proto_schedule.html", context=context)

def check_schedule(sched):
    for time_block in sched:
        for x in sched[time_block]:
            if x == 23:
                return True
    return False


def friendScheduleView(request, username):
    sched, created = Schedule.objects.get_or_create(user=request.user)
    # response = requests.get("https://luthers-list.herokuapp.com/api/dept/CS/?format=json").json()
    # course_list = [response[33], response[58], response[48], response[28]]
    # print(course_list[0])
    class_times = dict()  
    flag = 1 
    User = get_user_model()
    sched = Schedule.objects.filter(user=User.objects.filter(username=username).first())
    event_list = list(Event.objects.filter(schedule__in=sched))
    course_list = []
    for event in event_list:
        course_list.append(event.course)
    for course in course_list:
        # looks like 'meetings': [{'days': 'MoWeFr', 'start_time': '10.00.00.000000-05:00', 'end_time': '10.50.00.000000-05:00', 'facility_description': 'Rice Hall 340'}]

        class_name = course['subject'] + " " + course['catalog_number']
        times = course['meetings'][0]
        if times['start_time'] == '':
            continue
        start_time = datetime.strptime(times['start_time'][:5], '%H.%M')
        end_time = datetime.strptime(times['end_time'][:5], '%H.%M')
        # turn into blocks
        diff = timedelta(minutes=30)
        blocks = []
        time_ptr = start_time
        while time_ptr < end_time:
            blocks.append(datetime.strftime(time_ptr, "%I:%M %p"))
            time_ptr += diff
        days = parse_days(times['days'], flag)
        class_times[class_name] = [blocks, days]
        flag += 1

    time_blocks = dict()
    format = '%H:%M'
    for hour in range(8, 21):
        for minute in range(0, 60, 30):
            time_blocks[datetime.strftime(datetime.strptime('{:02d}:{:02d}'.format(hour, minute), format), "%I:%M %p")] = [0 for i in range(5)]
    # want dict with key = time and value = list of len 5 representing days
    # change values of days for each class to highlight the right days
    for c in class_times:
        first = True
        for block in class_times[c][0]:
            if first:
                time_blocks[block] = [c if class_times[c][1][x] != 0 else time_blocks[block][x] if time_blocks[block][x] != 0 else 0 for x in range(5)]
                # for x in class_times[c][1]:
                #     if x != 0:
                #         time_blocks[block] = c
                #     else:
                #         time_blocks[block] = 0
                first = False
            else:
                # print(time_blocks[block], "block")
                # print(class_times[c][1], "c1")
                time_blocks[block] = [x[0] if (isinstance(x[0], str) and x[1] == 0) else 23 if (isinstance(x[0], str) and x[1] != 0) or (x[0] != 0 and x[1]) else x[0]+x[1] for x in zip(time_blocks[block], class_times[c][1])] # add list marking days from course to current days 
                # for x in zip(time_blocks[block], class_times[c][1]):
                #     if type(time_blocks[block]) == str:
                #         continue
                #     time_blocks[block] = sum(x)
    context = {"time_blocks": time_blocks, "courses": course_list, "friend": User.objects.filter(username=username).first()}
    model = CommentText
    if request.method == 'POST':
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.schedule = sched[0]
            comment.save()  
            form = CommentForm()
            comments = list(CommentText.objects.filter(schedule__in=sched))
            context = {"time_blocks": time_blocks, "courses": course_list, "friend": User.objects.filter(username=username).first(), "form": form, "comments": comments}
            if check_schedule(time_blocks):
                return render(request, "schedule.html", context=context)
            return render(request, "proto_schedule.html", context=context)
    else:   
        form = CommentForm(request.POST)
        comments = list(CommentText.objects.filter(schedule__in=sched))
        context = {"time_blocks": time_blocks, "courses": course_list, "friend": User.objects.filter(username=username).first(), "form": form, "comments": comments}
        if check_schedule(time_blocks):
            return render(request, "schedule.html", context=context)
        return render(request, "proto_schedule.html", context=context)
    # post = get_object_or_404(Schedule, id=)
    # if request.method == 'POST':
    #     form = CommentForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         print()
    # else:
    #     form = CommentForm(request.POST)
    #     return render(request, 'proto_schedule.html', {
    #         'form': form
    #     }, context=context)


def parse_days(days_string, n):
    # helper function for schedule, turns string of MoTuWeThFr into list of 5 boolean values
    to_ret = [0 for i in range(5)]
    if "Mo" in days_string:
        to_ret[0] = n
    if "Tu" in days_string:
        to_ret[1] = n
    if "We" in days_string:
        to_ret[2] = n
    if "Th" in days_string:
        to_ret[3] = n
    if "Fr" in days_string:
        to_ret[4] = n
    return to_ret


def friendsView(request):
    friends = Friendship.objects.filter(person1=request.user)
    User = get_user_model()
    users = User.objects.all()
    friendRequests = FriendRequest.objects.filter(to_user=request.user)
    context = {'friends': friends,
               'friendRequests': friendRequests, 'users': users}
    return render(request, "friends.html", context=context)


def friendRequestView(request):
    friends = Friendship.objects.filter(person1=request.user)
    friendRequests = FriendRequest.objects.filter(from_user=request.user)
    User = get_user_model()
    users = User.objects.all()

    friends_friendRequests = []
    req = []

    for i in friends:
        friends_friendRequests.append(i.person2)

    for i in friendRequests:
        friends_friendRequests.append(i.to_user)
        req.append(i.to_user)

    context = {'users': users, 'friends': friends, 'friendRequests': req, 'friends_friendRequests': friends_friendRequests}

    # context = {'users': users, 'friends': friends, 'friendRequests': friendRequests}
    return render(request, "friendRequest.html", context=context)


def send_friend_request(request, userID):
    User = get_user_model()
    fromUser = request.user
    toUser = User.objects.get(id=userID)
    friend_request, created = FriendRequest.objects.get_or_create(
        from_user=fromUser, to_user=toUser)
    if created:
        return HttpResponseRedirect(reverse('friendRequests'))
    else:
        return HttpResponseRedirect(reverse('friendRequests'))

def unsend_friend_request(request, userID):
    User = get_user_model()
    fromUser = request.user
    toUser = User.objects.get(id=userID)
    friend_request = FriendRequest.objects.get(
        from_user=fromUser, to_user=toUser)
    friend_request.delete()
    return HttpResponseRedirect(reverse('friendRequests'))

def accept_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        Friendship.objects.get_or_create(
            person1=friend_request.from_user,
            person2=friend_request.to_user)
        Friendship.objects.get_or_create(
            person1=friend_request.to_user,
            person2=friend_request.from_user)
        friend_request.delete()
        return HttpResponseRedirect(reverse('friends'))
    else:
        return HttpResponseRedirect(reverse('friends'))


def deny_friend_request(request, requestID):
    friend_request = FriendRequest.objects.get(id=requestID)
    friend_request.delete()
    return HttpResponseRedirect(reverse('friends'))


def delete_friend(request, friendID):
    friendship1 = Friendship.objects.get(id=friendID)
    friendship2 = Friendship.objects.get(
        person1=friendship1.person2, person2=friendship1.person1)
    friendship1.delete()
    friendship2.delete()
    return HttpResponseRedirect(reverse('friends'))


def coursesView(request):
    return render(request, "courses.html")


def addClassView(request, subject, coursenum, department):
    response = requests.get("https://luthers-list.herokuapp.com/api/dept/" + subject + "/?format=json")
    data = response.json()
    correct_courses = [course for course in data if int(course['course_number']) == coursenum]               
    sched, created = Schedule.objects.get_or_create(user=request.user)
    courses_in_schedule = Event.objects.filter(schedule=sched)
    conflict = False

    incoming_subject = correct_courses[0]["subject"]
    incoming_catalog_number = correct_courses[0]["catalog_number"]
    
    # handles courses with no meeting times
    if correct_courses[0]["meetings"][0]["start_time"][0:2] == "": 
        # checks for any matches
        for c in Event.objects.filter(schedule=sched):
            json_course = c.course
            c_subject = json_course['subject']
            if c_subject == incoming_subject:
                print("not added")
                dept = get_object_or_404(Dept, dept_url_shorthand=department)
                return  HttpResponseRedirect(reverse('coursesDept', kwargs={'department': dept.dept_url_shorthand}))
        # no matching course subjects so add
        print("added")
        newclass, created = Event.objects.get_or_create(course=correct_courses[0], course_num=correct_courses[0]['course_number'], schedule=sched)
        dept = get_object_or_404(Dept, dept_url_shorthand=department)
        return HttpResponseRedirect(reverse('coursesDept', kwargs={'department': dept.dept_url_shorthand}))

    incoming_start_hour = int(correct_courses[0]["meetings"][0]["start_time"][0:2])
    incoming_start_min = int(correct_courses[0]["meetings"][0]["start_time"][3:5])
    incoming_end_hour = int(correct_courses[0]["meetings"][0]["end_time"][0:2])
    incoming_end_min = int(correct_courses[0]["meetings"][0]["end_time"][3:5])

    for i in courses_in_schedule:
        if correct_courses[0] == i.course or (incoming_subject == i.course["subject"] and incoming_catalog_number == i.course["catalog_number"]):
            print("same class")
            conflict = True
        # end time of the potential adding course has to be before the start time of the courses that are already in schedule
        # start time either :00 or :30
        # end hour < start hour
        if i.course["meetings"][0]["start_time"][0:2] == "":
            continue
        cis_start_hour = int(i.course["meetings"][0]["start_time"][0:2])
        cis_start_min = int(i.course["meetings"][0]["start_time"][3:5])
        cis_end_hour = int(i.course["meetings"][0]["end_time"][0:2])
        cis_end_min = int(i.course["meetings"][0]["end_time"][3:5])
        # incoming = mwf 12 - 12:50
        # already = mwf 12:30 - 1:15
        # conflict = True
        # incoming = mwf 12 - 12:50
        # already = mwf 1:00 - 1:50
        # conflict = False
        # incoming = mwf 1:30 - 1:50
        # already = mwf 12:30 - 1:45
        # conflict = True

        if incoming_end_hour == cis_start_hour and incoming_end_min < cis_start_min:
            # print("l1")
            conflict = False
        elif incoming_start_hour == cis_start_hour and correct_courses[0]["meetings"][0]["days"] in i.course["meetings"][0]["days"]:
            # print("l4")
            # print("hello")
            conflict = True
        elif incoming_end_hour > cis_start_hour and incoming_start_hour < cis_start_hour and correct_courses[0]["meetings"][0]["days"] in i.course["meetings"][0]["days"]:
            # print("l2")
            # print(incoming_end_hour, cis_start_hour)
            conflict = True
        elif incoming_end_hour == cis_start_hour and incoming_end_min >= cis_start_min and correct_courses[0]["meetings"][0]["days"] in i.course["meetings"][0]["days"]:
            # print("l3")
            conflict = True
        
        # print("incoming time:", incoming_start_hour, incoming_start_min, incoming_end_hour, incoming_end_min)
        # print("already time", cis_start_hour, cis_start_min, cis_end_hour, cis_end_min)
        # print(conflict)

    # print(courses_in_schedule)
    if not conflict:
        print("added")
        newclass, created = Event.objects.get_or_create(course=correct_courses[0], course_num=correct_courses[0]['course_number'], schedule=sched)
        dept = get_object_or_404(Dept, dept_url_shorthand=department)
        messages.info(request, 'Successfully added course to schedule')
        return HttpResponseRedirect(reverse('coursesDept', kwargs={'department': dept.dept_url_shorthand}))
    else:
        print("not added")
        dept = get_object_or_404(Dept, dept_url_shorthand=department)
        messages.error(request, 'Failed to add course to schedule')
        return HttpResponseRedirect(reverse('coursesDept', kwargs={'department': dept.dept_url_shorthand}))
    # return render(request, 'addclass.html', {'user': request.user, 'subject': subject, 'coursenum': coursenum})
    
def removeClassView(request, coursenum):
    sched = get_object_or_404(Schedule, user=request.user)
    Event.objects.filter(schedule=sched, course_num=coursenum).delete()
    return HttpResponseRedirect(reverse('schedule'))
    
def coursesDeptView(request, department):
    # response = requests.get("https://luthers-list.herokuapp.com/api/dept/ANTH/?format=json")
    # anth = response.json()
    # print(anth)
    dept = get_object_or_404(Dept, dept_url_shorthand=department)
    user = request.user
    course_list = []
    time = []
    counter = 0
    for subject in dept.subject_set.all():
        url = ''.join(['https://luthers-list.herokuapp.com/api/dept/',
                      subject.mnemonic, '/?format=json'])
        response = requests.get(url).json()

        if len(response) > 0:
            response[0]['subj_name'] = subject.subj_name
            course_list.append(response)

    if len(course_list) != 0:
        for subj in range(len(course_list)):
            total = len(course_list[subj])
            counter = 0
            while counter < total:
                c = course_list[subj]
                t = ""

                if len(c[counter].get('meetings')) == 0:
                    counter += 1
                    continue

                startL = c[counter].get('meetings')[0].get(
                    'start_time').partition('-')[0]
                if startL[0: 2] != "":
                    startHour = int(startL[0: 2])
                    if startHour >= 12:
                        if startHour != 12:
                            startHour = startHour - 12
                        start = str(startHour) + ":" + startL[3: 5] + " PM"
                    else:
                        start = str(startHour) + ":" + startL[3: 5] + " AM"
                else:
                    t = "-"
                endL = c[counter].get('meetings')[0].get(
                    'end_time').partition('-')[0]
                if endL[0:2] != "":
                    endHour = int(endL[0: 2])
                    if endHour >= 12:
                        if endHour != 12:
                            endHour = endHour - 12
                        end = str(endHour) + ":" + endL[3: 5] + " PM"
                    else:
                        end = str(endHour) + ":" + endL[3: 5] + " AM"
                else:
                    t = "-"
                if t != "-":
                    t = start + " - " + end
                # time.append(t)
                course_list[subj][counter]["time"] = t
                course_list[subj][counter]["rating"], created = CourseRating.objects.get_or_create(
                    course_num=course_list[subj][counter]['course_number'])
                user_rating = Rating.objects.filter(
                    course=course_list[subj][counter]["rating"], user=user).first()
                course_list[subj][counter]["user_rating"] = user_rating.rating if user_rating else "N/A"

                counter += 1
        
    # sched = get_object_or_404(Schedule, user=request.user)
    # courses_in_schedule = Event.objects.filter(schedule=sched)
    # print(courses_in_schedule)
    # cInSched = []
    # for i in courses_in_schedule:
    #     cInSched.append(i.course_num)
         # startR = c[0].get('meetings')[0].get('start_time').partition('-')[2]
    
    sched = Schedule.objects.filter(user=request.user)
    event_list = list(Event.objects.filter(schedule__in=sched))
    course_nums = []
    for event in event_list:
        course_nums.append(event.course_num)
    print(course_nums)
    return render(request, "coursesDept.html", {'dept': dept, 'data': course_list, 'added': course_nums})


def validateView(request, department, coursenum):
    course_rating = CourseRating.objects.get(course_num=coursenum)
    Rating.objects.filter(user=request.user, course=course_rating).delete()
    course_rating.rating_set.create(
        user=request.user, course=course_rating, rating=request.POST['rating'])
    dept = get_object_or_404(Dept, dept_url_shorthand=department)
    return HttpResponseRedirect(reverse('coursesDept', kwargs={'department': dept.dept_url_shorthand}))


def searchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST, request.FILES)
        if form.is_valid():
            response = requests.get("https://luthers-list.herokuapp.com/api/dept/" +
                                    form.cleaned_data['mnemonic'].upper() + "/?format=json")
            data = response.json()
            # print(data)
            correct_courses = [
                course for course in data if course['catalog_number'] == form.cleaned_data['course_num']]

            # Filter by Course Component
            total = len(correct_courses)
            counter = 0
            while counter < total:
                c = correct_courses
                t = ""

                if len(c[counter].get('meetings')) == 0:
                    counter += 1
                    continue

                startL = c[counter].get('meetings')[0].get(
                    'start_time').partition('-')[0]
                if startL[0: 2] != "":
                    startHour = int(startL[0: 2])
                    if startHour >= 12:
                        if startHour != 12:
                            startHour = startHour - 12
                        start = str(startHour) + ":" + startL[3: 5] + " PM"
                    else:
                        start = str(startHour) + ":" + startL[3: 5] + " AM"
                else:
                    t = "-"
                endL = c[counter].get('meetings')[0].get(
                    'end_time').partition('-')[0]
                if endL[0:2] != "":
                    endHour = int(endL[0: 2])
                    if endHour >= 12:
                        if endHour != 12:
                            endHour = endHour - 12
                        end = str(endHour) + ":" + endL[3: 5] + " PM"
                    else:
                        end = str(endHour) + ":" + endL[3: 5] + " AM"
                else:
                    t = "-"
                if t != "-":
                    t = start + " - " + end

                # time.append(t)
                correct_courses[counter]["time"] = t

                counter += 1

        if (form.cleaned_data['semester'] != ""):
            print("Filtering semesters")
            correct_courses = [course for course in correct_courses if course['semester_code'] == int(
                form.cleaned_data['semester'])]

        if (form.cleaned_data['component'] != ""):
            correct_courses = [
                course for course in correct_courses if course['component'] == form.cleaned_data['component']]

        if (not form.cleaned_data['credits'] == ""):
            correct_courses = [
                course for course in correct_courses if course['units'] == form.cleaned_data['credits']]

        if (len(form.cleaned_data['days']) > 0):
            for day in form.cleaned_data['days']:
                correct_courses = [
                    course for course in correct_courses if day in course['meetings'][0]['days']]

        if (form.cleaned_data['include_full_classes'] == "No"):
            print("filtering by availability")
            correct_courses = [
                course for course in correct_courses if course['enrollment_available'] > 0]

        return render(request, 'searchResults.html', {
            'data': correct_courses,
            'form': form
        })
    else:
        form = SearchForm(request.POST)
        return render(request, 'search.html', {
            'form': form
        })

class AddCommentView(generic.CreateView):
    model = CommentText
    form_class = CommentForm
    template_name = "addComment.html"
    success_url = reverse_lazy('schedule')

# def AddCommentFuncView(request):
#     if request.method == 'POST':
#         form=CommentForm(request.POST, request.FILES)
#         if form.is_valid():
#             return HttpResponseRedirect(reverse('schedule', kwargs={}), 'addComment.html', {
#                 'form': form
#             })
#     else:
#         form = CommentForm(request.POST, request.FILES)
#         return render(request, "addComment.html", {
#             'form': form
#         })


# class AddCommentSelfView(generic.CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "addComment.html"
#     success_url = reverse_lazy('friends')

# class AddCommentFriendView(generic.CreateView):
#     model = Comment
#     form_class = CommentForm
#     template_name = "addComment.html"
#     success_url = reverse_lazy('schedule')

#def index(request):
#    mnemonic = Search.objects.all()
#    context = {
#        'data': mnemonic
#    }
#    return render(request, 'searchView.html', context)

#class SearchView(generic.CreateView):
#    model = Search
#    template_name = "search.html"
#    fields = ['mnemonic', 'course_num']
#    
#    def form_valid(self, form):
#        form.save()
#        return redirect(reverse('search-results'))

        
