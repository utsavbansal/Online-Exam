from django import forms
from django.contrib.auth.forms import User,UserCreationForm,AuthenticationForm
from .models import Candidate

class SignUpForm(UserCreationForm):
	user_name=forms.CharField(max_length=30,required=True)
	first_name=forms.CharField(max_length=30,required=True)
	last_name=forms.CharField(max_length=30,required=True)
	email=forms.EmailField(max_length=254,help_text='Required.inform a valid email address.')
	course=forms.CharField(max_length=30)
	address=forms.CharField(max_length=50)
	age=forms.IntegerField()
	qualification=forms.CharField(max_length=20)
	password=forms.CharField(max_length=30,required=True,widget=forms.PasswordInput)
	class Meta:
		model=Candidate
		fields=['user_name','first_name','last_name','email','password','course','age','address','qualification']
		

class LoginForm(AuthenticationForm):
	username=forms.CharField(label="Username",max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'username'}))
	password=forms.CharField(label="Password",max_length=30,widget=forms.TextInput(attrs={'class':'form-control','name':'password'}))

	
class SignUp(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	
	class Meta:
		model=Candidate
		fields=['user_name','first_name','last_name','email','password','course','age','address','qualification']
	    