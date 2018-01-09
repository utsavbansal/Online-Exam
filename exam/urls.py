from django.conf.urls import url
from .forms import LoginForm
from . import views
app_name='exam'
urlpatterns=[
	url(r'^login/$',views.login.as_view(),name='login'),
	url(r'^signup/$',views.UserFormView.as_view(),name='signup'),
	url(r'^home/$',views.home,name='home'),
	url(r'^login/$',views.login,name='login'),
	url(r'^testcase1/$',views.testcase1,name='testcase1'),
	url(r'^(?P<question_id>[0-9]+)/$',views.testcase_detail,name='testcase_detail'),
	url(r'^result/$',views.result,name='result'),
	url(r'^(?P<question_id>[0-9]+)/store_answer/$',views.store_answer,name='store_answer'),
]