# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Question,Candidate,Candidate_Choice,Choice
# Register your models here.

class ChoiceInline(admin.TabularInline):
	model=Choice
	extra=4
class QuestionAdmin(admin.ModelAdmin):
	search_fields=['question_text']
	list_filter=['pub_date','category']
	list_display=('question_text','pub_date','was_published_recently','is_ejected')
	fieldsets=[
	(None, {'fields':['question_text','answer','category','marks','eject_field']}),
	('Date Information', {'fields':['pub_date']}),
	]
	inlines=[ChoiceInline]
	
admin.site.register(Question,QuestionAdmin)

class Candidate_Choice_Inline(admin.TabularInline):
	model=Candidate_Choice
	extra=1
	
class CandidateAdmin(admin.ModelAdmin):
	search_fields=['first_name']
	list_filter=['passed','marks','first_name','eject_field','age']
	list_display=('__str__','email','age','marks','is_ejected','is_passed')
	fieldsets=[
	(None,{'fields':['first_name','last_name','user_name','password','course','address','age','qualification','email','eject_field','marks','passed']}),
	]
	inlines=[Candidate_Choice_Inline]

admin.site.register(Candidate,CandidateAdmin)

