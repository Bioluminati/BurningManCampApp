"""bioluminati URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from camp.views import index, signup, profile, register, bike_form, bikemutation, inventory, about
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', index, name='index'),
    url(r'^signup/', signup, name='signup'),
    url(r'^accounts/profile/$', profile, name='profile'),
    # url(r'^accounts/campers/$', campers, name='campers'), make profile display page
    url(r'^login/', 'django.contrib.auth.views.login', name='foo',kwargs={'template_name': 'login.html'}),
    url(r'^/logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    url(r'^register/$', register, name='register'),
    url(r'^confirm/$', register, name='confirm'),  
    url(r'^bikes/$', bike_form, name='bikes'),  
    url(r'^bikemutation/$', bikemutation, name='bikemutation'), 
    url(r'^inventory/$', inventory, name='inventory'), 
    url(r'^about/$', about, name='about'), 
     # url(r'^about/$', TemplateView.as_view(template_name="about.html"), name='about')
    # url(r'^accounts/', include('django.contrib.auth.urls')),
]
