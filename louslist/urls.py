from django.urls import path, include
from django.contrib.auth.views import LogoutView
from . import views
from .views import AddCommentView

urlpatterns = [
    path("", views.homeView, name="home"),
    path("home/", views.homeView, name="home"),
    path("logout", LogoutView.as_view(), name="logout"),
    #login page
    path("login/", views.login, name="login"),
    path("", include("allauth.urls")),
    #schedule page
    #have to change to the commented out one for user specific schedule
    path("schedule/", views.scheduleView, name="schedule"),
    path("schedule/add_class/<str:subject>/<int:coursenum>/<str:department>/", views.addClassView, name="addClass"),
    path("schedule/remove_class/<int:coursenum>/", views.removeClassView, name="removeClass"),
    path("schedule/<str:username>/", views.friendScheduleView, name="friendSchedule"),

    #friends page
    #have to change to the commented out one for user specific friends
    path("friends/", views.friendsView, name = "friends"),
    path("friends/delete_friend/<int:friendID>/", 
        views.delete_friend, name='delete friend'),

    path("friends/request", views.friendRequestView, name= "friendRequests"),
    #path("friends/<int:computing_id>/", views.friendsView, name = "friends"),
    path("friends/request/send_friend_request/<int:userID>/", 
        views.send_friend_request, name='send friend request'),
    path("friends/request/unsend_friend_request/<int:userID>/", 
        views.unsend_friend_request, name='unsend friend request'),
    path("friends/request/accept_friend_request/<int:requestID>/",
        views.accept_friend_request, name='accept friend request'),
    path("friends/request/deny_friend_request/<int:requestID>/",
        views.deny_friend_request, name='deny friend request'),
    #all courses page
    path("courses/", views.coursesView, name = "courses"),
    #specific courses page (ex: cs courses only)
    path("courses/<str:department>/", views.coursesDeptView, name = "coursesDept"),
    #path("courses/cs/", views.csCourse, name = "coursesDept"),

    #search page
    path("search/", views.searchView, name = "search"),
    #path("search-results/", views.searchResultView, name = "search-results"),
    path("validate/<str:department>/<int:coursenum>/", views.validateView, name="validate"),
    # path("schedule/<str:usernamecomment/",views.AddCommentView.as_view(), name= "add_comment_self"),
    path("schedule/<str:username>/comment/", views.AddCommentView.as_view(), name = "add_comment")
]
