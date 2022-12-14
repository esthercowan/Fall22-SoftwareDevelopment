"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import requests

api_url = "http://luthers-list.herokuapp.com/api/dept/CS"
response = requests.get(api_url)
list = response.json()

instructor = []
for i in list:
    instructor.append(i.get("instructor"))


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("louslist.urls")),
]
