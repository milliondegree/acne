# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class User(models.Model):
	Username = models.CharField(max_length=20)
	Password = models.CharField(max_length=20)
	Authority = models.IntegerField()
	def __str__(self):
		return self.Username
		
class Image(models.Model):
	Iname = models.CharField(max_length=20)
	#Icontext=models.ImageField(upload_to='photos')
	Iuser=models.ForeignKey(User)
	def __str__(self):
		return self.Iname
		
		
class Patient(models.Model):
	Name=models.CharField(max_length=20)
	Pid=models.CharField(max_length=20)
	def __str__(self):
		return self.Name