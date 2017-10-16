#coding=utf-8
from django import forms

class UserFormLogin(forms.Form):
	username = forms.CharField(required=False, label='Username',max_length=20,widget=forms.TextInput())  
	password = forms.CharField(required=False, label='Password',max_length=20,widget=forms.PasswordInput())  
	
class ImageForm(forms.Form):
	#title=forms.CharField(required=False, max_length=50)
	image=forms.ImageField(required=False,widget=forms.ClearableFileInput())
	
class ChooseForm(forms.Form):
	username=forms.CharField(required=False,label='Username',max_length=20,widget=forms.TextInput())
