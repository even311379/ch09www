# -*- coding: utf-8 -*-
import json
from django.utils.encoding import smart_text
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect
from django.core.mail import send_mail, EmailMessage
from mysite import models , forms
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.


def post_remove(request,pk):
	post= get_object_or_404(models.Post,pk=pk)
	post.delete()
	return HttpResponseRedirect('/')
# REF: https://stackoverflow.com/questions/37532140/delete-object-on-click

def index(request, pid = None, del_pass=None):
	HOME = True
	# if 'username' in request.COOKIES and 'usercolor' in request.COOKIES:
	# 	username = eval(request.COOKIES['username']) 
	# 	usercolor = eval(request.COOKIES['usercolor'])

	# if 'username' in request.session:
	# 	username = request.session['username']
	# 	useremail = request.session['useremail']

	if request.user.is_authenticated:
		username = request.user.username
		try:
			fuser = User.objects.get(username=username)
			print(type(fuser))
			Diaries = models.Diary.objects.filter(user=fuser).order_by('-ddate')
		except Exception as e:
			print(e)
	messages.get_messages(request)

	return HttpResponse(render(request,'../templates/index.html',locals()))

def listing(request):
	template = get_template('listing.html')
	posts = models.Post.objects.filter(enabled = True).order_by('-pub_time')[:150]
	Lp = len(posts)
	LIST = True
	moods = models.Mood.objects.all()
	html = template.render(locals())

	return HttpResponse(html)

@login_required(login_url = '/login')
def posting(request):
	if request.user.is_authenticated:
		username = request.user.username
		useremail = request.user.email
	messages.get_messages(request)

	if request.method == 'POST':
		fuser = User.objects.get(username=username)
		form = forms.DiaryForm(request.POST)
		# diary = models.Diary(user=user)
		# post_form = forms.DiaryForm(request.POST, instance=diary)
		# if post_form.is_valid():
		if form.is_valid():
			try:
				fbudget = form.cleaned_data['budget']
				fweight = form.cleaned_data['weight']
				fnote = form.cleaned_data['note']
				fdate = request.POST.get("DiaryDate",None)
				ds=fdate.split('/')
				fdate = ds[2]+'-'+ds[0]+'-'+ds[1]
				Diary = models.Diary.objects.create(user=fuser,budget=fbudget,weight=fweight,note=fnote,ddate=fdate)
				Diary.save()

				messages.add_message(request, messages.INFO, "日記已儲存")
				# post_form.save()
				return HttpResponseRedirect('/')
			# else:
			except Exception as e:
				print(e)
				messages.add_message(request, messages.WARNING, "Something worng!")
			# print(budget)
	else:
		post_form = forms.DiaryForm()
		messages.add_message(request, messages.INFO, "請寫下日記!")

	return HttpResponse(render(request,'../templates/posting.html',locals()))


def contact(request):
	CONT = True
	if request.method == 'POST':
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			user_name = form.cleaned_data['user_name']
			user_city = form.cleaned_data['user_city']
			user_email = form.cleaned_data['user_email']
			user_message = form.cleaned_data['user_message']


			mail = EmailMessage('來自{0} 城市的{1} 網友的寶貴意見'.format(user_city,user_name),user_message,user_email,['even311379@gmail.com'])
			# hotmail will block mails from mailgun, but it works fine on gmail!
			mail.send()
	else:
		form = forms.ContactForm()
	return HttpResponse(render(request,'../templates/contact.html',locals()))


def post2db(request):
	POSTDB = True
	if request.method == 'POST':
		post_form = forms.PostForm(request.POST)
		if post_form.is_valid():
			message = '成功！'
			post_form.save()
			return HttpResponseRedirect('/list')
	else:
		post_form = forms.PostForm()
		message = '如果要po文，每個欄位都要填喔！'
	return HttpResponse(render(request,'../templates/post2db.html',locals()))


	
# def login(request):
# 	LOGI = True
# 	username = None
# 	usercolor = None
# 	if request.method == 'POST':
# 		login_form = forms.LoginForm(request.POST)
# 		if login_form.is_valid():
# 			username = request.POST['user_name']
# 			usercolor = request.POST['user_color']
# 			message = '登入成功！'
# 		else:
# 			message = '登入失敗，請檢查欄位。'

# 		# return HttpResponseRedirect('/')
# 	else:
# 		login_form = forms.LoginForm()

# 	response = HttpResponse(render(request,'../templates/login.html',locals()))

# 	if username:
# 		response.set_cookie(key='username', value=json.dumps(username,ensure_ascii=True),max_age=3600)
# 	if usercolor:
# 		response.set_cookie(key='usercolor', value=json.dumps(usercolor),max_age=3600)


# 	return response

def login(request):
	LOGI = True

	if request.method == 'POST':
		login_form = forms.LoginForm(request.POST)
		if login_form.is_valid():
			login_name = request.POST['username'].strip()
			login_password = request.POST['password']
			try:
				# this is session login
				'''
				user = models.User.objects.get(name=login_name)
				if user.password == login_password:
					
					request.session['username'] = user.name
					request.session['useremail'] = user.email
					messages.add_message(request, messages.SUCCESS,'成功登入了')
					return HttpResponseRedirect('/')
				'''

				# this is django login module
				user = authenticate(username = login_name,password = login_password)
				if user:
					if user.is_active:
						auth.login(request, user)
						print('success')
						messages.add_message(request, messages.SUCCESS,'成功登入了')
						return HttpResponseRedirect('/')

				else:
					messages.add_message(request, messages.WARNING, '密碼錯誤')
			except:
				messages.add_message(request, messages.WARNING, 'Something wrong! This user does not exist.')
		else:
			messages.add_message(request, messages.WARNING,'登入失敗，請檢查欄位。')

	else:
		login_form = forms.LoginForm()

	response = HttpResponse(render(request,'../templates/login.html',locals()))

	return response



def logout(request):
	response = HttpResponseRedirect('/')
	# response.delete_cookie('username')
	# del request.session['username']
	auth.logout(request)
	messages.add_message(request, messages.INFO, "成功登出了")

	return response

@login_required(login_url='/login')
def userinfo(request):
	USINF = True
	# if 'username' in request.session:
	# 	username = request.session['username']
	# 	useremail = request.session['useremail']
	# else:
	# 	return HttpResponseRedirect('/login')
	# try:
	# 	userinfo = models.User.objects.get(name=username)
	# except:
	# 	print('fail')

	if request.user.is_authenticated:
		username = request.user.username
		try:
			user = User.objects.get(username=username)
			userinfo = models.Profile.objects.get(user=user)
		except:
			pass

	return HttpResponse(render(request,'../templates/userinfo.html',locals()))