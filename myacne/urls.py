from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$',views.userlogin,name='login'),
	url(r'^index/$',views.index,name='index'),
	url(r'^sign/$',views.sign,name='sign'),
	url(r'^browse/$',views.browse,name='browse')
]
