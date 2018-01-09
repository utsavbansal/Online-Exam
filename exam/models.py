# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.db import models
from django.utils import timezone

from django.utils.encoding import python_2_unicode_compatible
# Create your models here.
@python_2_unicode_compatible
class Question(models.Model):
	question_image=models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')
	question_text=models.CharField(max_length=200)
	answer=models.CharField(max_length=50)
	category=models.CharField(max_length=10)
	pub_date=models.DateTimeField('date published')
	marks=models.PositiveSmallIntegerField()
	choice1=models.CharField(max_length=200)
	choice2=models.CharField(max_length=200)
	choice3=models.CharField(max_length=200)
	eject_field=models.BooleanField(default=False)
	def is_ejected(self):
		return self.eject_field
	def __str__(self):
		return self.question_text
	def was_published_recently(self):
		now=timezone.now()
		return self.pub_date>= timezone.now()-datetime.timedelta(days=1)
	was_published_recently.admin_order_field='pub_date'
	was_published_recently.boolean=True
	was_published_recently.short_description='Published Recently'
	is_ejected.boolean=True
	
@python_2_unicode_compatible
class Choice(models.Model):
	question=models.ForeignKey(Question,on_delete=models.CASCADE)
	choice_text=models.CharField(max_length=200)
	def __str__(self):
		return self.choice_text
class Candidate(models.Model):
	first_name=models.CharField(max_length=30)
	last_name=models.CharField(max_length=30)
	user_name=models.CharField(max_length=30)
	password=models.CharField(max_length=30)
	course=models.CharField(max_length=30)
	address=models.CharField(max_length=50)
	age=models.PositiveSmallIntegerField()
	qualification=models.CharField(max_length=20)
	email=models.EmailField(max_length=254)
	eject_field=models.BooleanField()
	marks=models.PositiveIntegerField(default=0)
	passed=models.BooleanField(default=False)
	def __str__(self):
			return self.first_name+" "+self.last_name
	def is_ejected(self):
		return self.eject_field
	def is_passed(self):
		return self.passed
	is_ejected.boolean=True
	is_passed.boolean=True
class Candidate_Choice(models.Model):
	candidate_name=models.ForeignKey(Candidate,on_delete=models.CASCADE)
	candidate_question=models.CharField(max_length=200,default=None)
	candidate_answer=models.CharField(max_length=200,default=None)

	def __str__(self):
			return self.candidate_name.first_name+" "+self.candidate_name.last_name