# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from random import shuffle
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect,get_object_or_404
from django.template import loader
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Candidate,Choice
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,SignUp,LoginForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import generic
from django.views.generic import View
		
#@login_required(login_url="login/")

class login(View):
	form_class=LoginForm
	template_name='exam/login.html'
	
	# display blank form
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})
	# process form data
	def post(self,request):
		form=self.form_class(request.POST)
	
		if form.is_valid():
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			
			# return user objects if credentials are coorect
			user=authenticate(user_name=username,password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					# request.user to get  data from user object
					return redirect('exam:home')
		else:
			HttpResponse("wrong")
		return render(request,self.template_name,{'form':form})
	
	
	
	'''
	username=request.POST['username']
	password=request.POST['password']
	user=authenticate(request,username=username,password=password)
	if user is not None:
		login(request,user)
	'''
		
def logout_user(request):
	logout(request)
def home(request):
	testcase=Question.objects.order_by('marks')[:10]
	template=loader.get_template('exam/home.html')
	context={
		'testcase':testcase,
	}
	return HttpResponse(template.render(context,request))
	
def testcase1(request):
	question_list=[]
	count=1
	easy_question=Question.objects.filter(category='easy')[:]
	inter_question=Question.objects.filter(category='inter')[:]
	hard_question=Question.objects.filter(category='hard')[:]
	for i in easy_question:
		if i.eject_field==False:
			if count<=10:
				question_list.append(i)
				count+=1
	count=1
	for i in inter_question:
		if i.eject_field==False:
			if count<=5:
				question_list.append(i)
				count+=1
	count=1
	for i in hard_question:
		if i.eject_field==False:
			if count<=5:
				question_list.append(i)
				count+=1
	#for shuffling questions
	''' 
	index_easy=[i for i in range(0,len(easy_question))]
	shuffle(index_easy)
	
	index_inter=[i for i in range(0,len(inter_question))]
	shuffle(index_inter)
	
	index_hard=[i for i in range(0,len(hard_question))]
	shuffle(index_hard)
	for i in index_easy:
		if count<=10:
			question_list.append(easy_question[i])
			count+=1
	count=0
	for i in index_inter:
		if count<=5:
			question_list.append(inter_question[i])
			count+=1
	count=0
	for i in index_hard:
		if count<=5:
			question_list.append(hard_question[i])
			count+=1
	'''
	candidate=get_object_or_404(Candidate,pk=1)
	if candidate.eject_field==False:
		template=loader.get_template('exam/testcase1.html')
		context={
			'question_list':question_list,
		}
		return HttpResponse(template.render(context,request))
	else:
		template=loader.get_template('exam/testcase1.html')
		context={
			'error_message':"Sorry! You are not eligible to attend test,Please Contact Administrator",
		}
		return HttpResponse(template.render(context,request))
	
def testcase_detail(request,question_id):
	question=get_object_or_404(Question,pk=question_id)
	return render(request,'exam/testcase_detail.html',{ 'question':question})
	
	
def store_answer(request,question_id):
	obj=None
	question=get_object_or_404(Question,pk=question_id)
	question_list=Question.objects.order_by('marks')[:10]
	try:
		selected_choice=question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		return render(request,'exam/testcase_detail.html',{'question':question, 'error_message':"You didn't select a choice, Please Enter a Choice or hit back to go back"})
	else:
		candidate=get_object_or_404(Candidate,pk=1)
		candidate_question_list=candidate.candidate_choice_set.all()
		for i in candidate_question_list:
			if str(question.question_text)==str(i.candidate_question):
				obj=i
				break
		
		if obj!=None and str(question.question_text) == str(obj.candidate_question):					#if candidate has attended question
			#candidate_question_list=candidate.candidate_choice_set.filter(candidate_question__startswith=str(question))		#find the question
			if str(selected_choice)==str(question.answer) and str(selected_choice)!=str(obj.candidate_answer) :    #if candidate answer was previously wrong
				candidate.marks+=question.marks
				obj.candidate_answer=str(selected_choice)
				obj.save()
			elif str(selected_choice)!=str(question.answer) and str(question.answer)==str(obj.candidate_answer): 		##if candidate answer was previously right
				candidate.marks-=question.marks
				if candidate.marks<0:
					candidate.marks=0
				obj.candidate_answer=str(selected_choice)
				obj.save()
			else:
				obj.candidate_answer=str(selected_choice)
				obj.save()
				
		else:	# if candidate has not attended question before
			candidate.candidate_choice_set.create(candidate_question=question.question_text,candidate_answer=selected_choice)			# add details of question for candidate 
			if str(selected_choice)==str(question.answer):											#if answer is right
				candidate.marks+=question.marks
		
		
		
		
		candidate.save()
		
		return HttpResponseRedirect(reverse('exam:testcase1'))
		
		
		
def result(request):
	candidate=get_object_or_404(Candidate,pk=1)
	percentage=(100*candidate.marks)/35
	if percentage >= 30:
		candidate.passed=True
		candidate.save()
		return render(request,'exam/result.html',{'candidate':candidate,'result':"Congratulations! You are passed"})
	else:
		candidate.passed=False
		candidate.save()
		return render(request,'exam/result.html',{'candidate':candidate,'result':"Sorry! You are failed",'percentage':percentage})

'''def signup(request):
	if request.method=='POST':
		form=SignUpForm(request.POST)
		if form.is_Valid():
			form.save()
			username=form.cleaned_data.get('user_name')
			raw_password=form.cleaned_data.get('password')
			user=authenticate(username=username,password=raw_password)
			login(request,user)
			return redirect('home')
		else:	
			form=SignUpForm()
		return render(request,'exam/signup.html',{'form':form})

'''	
class UserFormView(View):
	form_class=SignUpForm
	template_name='exam/registration_form.html'
	
	# display blank form
	def get(self,request):
		form=self.form_class(None)
		return render(request,self.template_name,{'form':form})
	# process form data
	def post(self,request):
		form=self.form_class(request.POST)
	
		if form.is_valid():
			user=form.save(commit=False)
			
			#clean (normalised) data
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			user.set_password(password)
			user.save()
			
			# return user objects if credentials are coorect
			user=authenticate(user_name=username,password=password)
			if user is not None:
				if user.is_active:
					login(request,user)
					# request.user to get  data from user object
					return redirect('exam:home')
		else:
			HttpResponse("wrong")
		return render(request,self.template_name,{'form':form})
	
	
	
	
	
	
	
	
	
	
	
	
	