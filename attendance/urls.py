"""
URL configuration for zkcvapi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from attendance import views

urlpatterns = [
    path('', views.input_unenroll, name="input_unenroll"),
    path('upload', views.upload_unenroll),
    path('clock_unenroll', views.clock_unenroll, name="clock_unenroll"),
    path('emp_enroll', views.emp_enroll, name="emp_enroll"),
    path('upload_enroll', views.upload_enroll, name="upload_enroll"),
]
