"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.register, name='register'),
    url(r'login/', views.login, name='login'),
    url(r'profile/(?P<id>[0-9]+)/', views.profile, name='profile'),
    url(r'addPassword/(?P<id>[0-9]+)/', views.addPassword, name='addPassword'),
    url(r'otp_request_page/', views.render_otp_request_page, name='otp_request_page'),
    url(r'one_time_password_request/',views.sendOTP,name="one_time_password_request"),
    url(r'one_time_password_enter/(?P<username>[A-Za-z0-9_-]{3,20})/',views.render_otp_input_page,name="one_time_password_enter"),
    url(r'change_password/(?P<username>[A-Za-z0-9_-]{3,20})/', views.change_password_view, name='change_password'),
]
