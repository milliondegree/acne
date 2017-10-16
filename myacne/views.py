# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import json
import base64
from Predictor import *
from django.shortcuts import render,render_to_response
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .forms import UserFormLogin,ImageForm
from django.template import RequestContext 
from django.contrib import auth  
from .models import User, Image
from django.views.decorators.csrf import csrf_protect
from acne import settings
import matplotlib.image as mpimg

p = Predictor('/home/zjc/acne/myacne/keras_model/bottleneck_fc_model_architecture.json',
    '/home/zjc/acne/myacne/keras_model/bottleneck_fc_model_weights.h5',
    '/home/zjc/acne/myacne/keras_model/top_seven_model_architecture.json',
    '/home/zjc/acne/myacne/keras_model/top_seven_model_weights.h5'
)

#@csrf_protect
def userlogin(request):
	if request.method=='POST':
		uf=UserFormLogin(request.POST)
		#return HttpResponse("post ok")
		if uf.is_valid():
			#return HttpResponse("the uf is valid")
			username=uf.cleaned_data['username']
			password=uf.cleaned_data['password']
			if username and password:
				userResult=User.objects.filter(Username=username,Password=password)
				if userResult[0]:
					if userResult[0].Authority==0:
						response = HttpResponseRedirect('/choose/')
						response.set_cookie('username',username,3600)
						return response
					
					else:
						response = HttpResponseRedirect('/picture/')
						response.set_cookie('username',username,3600)
						return response
					
				else:
					return HttpResponse("Can't find the user")
			
			else:
				uf=UserFormLogin();
	
	else:
		uf=UserFormLogin()
    
	return render_to_response('myacne/login.html',{'uf':uf})
            
      
  
def index(request):
	if request.method=='POST':
		
		#for convienence
		#print request.body
		#print request.read()
		#print request.is_ajax()
		#print request.META
		#print request.POST
		#print request.POST.dict()
		#print settings.DATA_UPLOAD_MAX_NUMBER_FIELDS
		#print request.FILES
		
		#get information from the request
		username=request.COOKIES.get('username','')
		files=request.FILES.getlist('myimage')
		
		# judge whether 'myimage' list is empty
		if not files:
			print "Catch it, bitch!"
			try:
				filedata = base64.b64decode(request.POST.get('file'))
				length=len(os.listdir('/home/zjc/acne/media/'+username+'/uncertain'))
				filename = str(length)+'.jpg'
				oneimage=Image(Iname='uncertain'+filename,Iuser=User.objects.get(Username=username))
				oneimage.save();
				fout = open('/home/zjc/acne/media/'+username+'/uncertain/'+filename, 'wb+')
				fout.write(filedata)
				fout.close()
			except:
				return JsonResponse({'status': 2})
			
			# code for Predictor
			try:
				bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
				return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})
			except:
				return JsonResponse({'status': 1})

			# bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
			# return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})

			# code for predictor
			# img = mpimg.imread('/home/zjc/acne/media/'+username+'/uncertain/'+filename)
			# ratio = predictor.predict(img)
			# class0 = ratio[0]
			# class1 = ratio[1]
			# class2 = ratio[2]
			# class3 = ratio[3]
			# return JsonResponse({'class0': class0, 'class1': class1, 'class2': class2, 'class3': class3})
			
			
		else:
			if len(files) >1:
				return JsonResponse({'status': 3})
			try:
				file = files[0];
				length=len(os.listdir('/home/zjc/acne/media/'+username+'/uncertain'))
			 	filename = str(length)+'.jpg'
			 	oneimage=Image(Iname='uncertain'+filename,Iuser=User.objects.get(Username=username))
			 	oneimage.save();
			 	destination=open('/home/zjc/acne/media/'+username+'/uncertain/'+filename,'wb+')
			 	for chunk in file.chunks(): 
			 		destination.write(chunk)
			 	destination.close()
			 	img = mpimg.imread('/home/zjc/acne/media/'+username+'/uncertain/'+filename)
			except:
				return JsonResponse({'status': 2})
			
			# code for Predictor
			try:
				bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
				return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})
			except:
				return JsonResponse({'status': 1})

			# bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
			# return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})
			
			# when recieve single image
			# if len(files) == 1:
			# 	file = files[0]
			# 	imagetype=file.name[0:2]
			# 	#process the signed image
			# 	if imagetype == 'nz' or imagetype == 'nb' or imagetype == 'ht' or imagetype == 'bt' or imagetype == 'qz' or imagetype == 'jj':
			# 		length=len(os.listdir('/home/zjc/acne/media/'+username+'/'+imagetype))
			# 		filename = str(length)+'.jpg'
			# 		oneimage=Image(Iname=imagetype+filename,Iuser=User.objects.get(Username=username))
			# 		oneimage.save();
			# 		destination=open('/home/zjc/acne/media/'+username+'/'+imagetype+'/'+filename,'wb+')
			# 		for chunk in file.chunks(): 
			# 			destination.write(chunk)
			# 		destination.close()
			# 		return JsonResponse({'status': 2})
				
			# 	#process the unsigned image
			# 	else:
			# 		length=len(os.listdir('/home/zjc/acne/media/'+username+'/uncertain'))
			# 		filename = str(length)+'.jpg'
			# 		oneimage=Image(Iname='uncertain'+filename,Iuser=User.objects.get(Username=username))
			# 		oneimage.save();
			# 		destination=open('/home/zjc/acne/media/'+username+'/uncertain/'+filename,'wb+')
			# 		for chunk in file.chunks(): 
			# 			destination.write(chunk)
			# 		destination.close()
			# 		img = mpimg.imread('/home/zjc/acne/media/'+username+'/uncertain/'+filename)
					
			# 		# code for Predictor
			# 		try:
			# 			bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
			# 			return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})
			# 		except:
			# 			return JsonResponse({'status': 1})

			# 		# bt_ratio, ht_ratio, qz_ratio, nb_ratio, nz_ratio, jj_ratio, abnormal_ratio = p.seven_classify(p.binary_classify(p.cut_image('/home/zjc/acne/media/'+username+'/uncertain/'+filename)))
			# 		# return JsonResponse({'status': 0, 'bt_ratio': bt_ratio, 'ht_ratio': ht_ratio, 'qz_ratio': qz_ratio, 'nb_ratio': nb_ratio, 'nz_ratio': nz_ratio, 'jj_ratio': jj_ratio, 'abnormal_ratio': abnormal_ratio})

			
			# #when recieve multiple images
			# else:
			# 	for file in files:
			# 		imagetype=file.name[0:2]
			# 		if imagetype == 'nz' or imagetype == 'nb' or imagetype == 'ht' or imagetype == 'bt' or imagetype == 'qz' or imagetype == 'jj':
			# 			length=len(os.listdir('/home/zjc/acne/media/'+username+'/'+imagetype))
			# 			filename = str(length)+'.jpg'
			# 			oneimage=Image(Iname=imagetype+filename,Iuser=User.objects.get(Username=username))
			# 			oneimage.save();
			# 			destination=open('/home/zjc/acne/media/'+username+'/'+imagetype+'/'+filename,'wb+')
			# 			for chunk in file.chunks(): 
			# 				destination.write(chunk)
			# 			destination.close()
			# 		else:
			# 			length=len(os.listdir('/home/zjc/acne/media/'+username+'/uncertain'))
			# 			filename = str(length)+'.jpg'
			# 			oneimage=Image(Iname=imagetype+filename,Iuser=User.objects.get(Username=username))
			# 			oneimage.save();
			# 			destination=open('/home/zjc/acne/media/'+username+'/uncertain/'+filename,'wb+')
			# 			for chunk in file.chunks(): 
			# 				destination.write(chunk)
			# 			destination.close()
			# 	return JsonResponse({'status': 2})
		
	else:
		iform=ImageForm()
	
	username=request.COOKIES.get('username','')
	return render_to_response('myacne/index_highcharts.html',{'username':username})
	
	
def choose(request):
	
	username=request.COOKIES.get('username','')
	if request.method=='POST':
		chozen=request.POST.get('chozen_user')
		ausername=request.POST.get('username')
		password=request.POST.get('password')
		
		if ausername!=None:
			newuser=User(Username=ausername,Password=password,Authority=1)
			newuser.save()
			os.makedirs('/home/zjc/acne/media/'+ausername)
			
		else:
			response = HttpResponseRedirect('/browse/')
			response.set_cookie('chozen_user',chozen,3600)
			return response
			
	list=[]
	userlist=User.objects.filter(Authority=1)
	for user in userlist:
		list.append(user.Username)
	return render_to_response('myacne/choose.html',{'username':username,'list':list})
    
	
def sign(request):
	username=request.COOKIES.get('username','')
	return render_to_response('myacne/sign.html',{'username':username})
	
def browse(request):
	chozen_user=request.COOKIES.get('chozen_user','')
	picnum=len(os.listdir('/home/zjc/acne/media/'+chozen_user))
	return render_to_response('myacne/browse.html',{'chozen_user':chozen_user,'picnum':json.dumps(picnum)})
#def add(request,a,b):
#   c=int(a)+int(b)
#   return HttpResponse(str(c))


# Create your views here.
