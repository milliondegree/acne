"""acneclassifier URL Configuration

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
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from myacne import views
from acne import settings
from django.conf.urls.static import static

urlpatterns = [
    #url(r'^add/(\d+)/(\d+)/$',myacne_views.add,name='add'),
    url(r'^admin/', admin.site.urls),
	url(r'^$',views.userlogin,name='login'),
	url(r'^picture/$',views.index,name='index'),
	url(r'^sign/$',views.sign,name='sign'),
	url(r'^browse/$',views.browse,name='browse'),
	url(r'^choose/$',views.choose,name='choose')
    #url(r'^acne/',include('myacne.urls')),   
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
