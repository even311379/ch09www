# -*- coding: utf-8 -*-
from django import forms
from mysite import models
from captcha.fields import CaptchaField
from django.contrib.admin import widgets
from bootstrap_datepicker.widgets import DatePicker

class ContactForm(forms.Form):
	CITY = [
	['TP','台北'],
	['TY','桃園'],
	['TC','台中'],
	['TN','台南'],
	['KA','高雄'],
	['NA','其他'],
	]

	user_name = forms.CharField(label = '您的名字',max_length=50,initial='王大明')
	user_city = forms.ChoiceField(label = '居住城市',choices=CITY)
	user_school = forms.BooleanField(label = '是否在學',required=False)
	user_email = forms.EmailField(label = '電子郵件',initial='even311379@hotmail.com')
	user_message = forms.CharField(label = '您的意見',widget=forms.Textarea,initial='TESTEST')


class PostForm(forms.ModelForm):
	captcha = CaptchaField()
	class Meta:
		model = models.Post
		fields = ['mood','nickname','message','del_pass','enabled']

	def __init__(self, *args, **kwargs):
		super(PostForm,self).__init__(*args, **kwargs)
		self.fields['mood'].label = '現在心情'
		self.fields['nickname'].label = '暱稱'
		self.fields['message'].label = '心情留言'
		self.fields['del_pass'].label = '設定密碼'
		self.fields['enabled'].label = '立刻刊登？'
		self.fields['captcha'].label = '機器人？'

class LoginForm(forms.Form):
	username = forms.CharField(label = '姓名', max_length = 10)
	password = forms.CharField(label= '密碼', widget=forms.PasswordInput())


# class LoginForm(forms.Form):
# 	COLORS = [
# 	['紅','紅'],
# 	['黃','黃'],
# 	['綠','綠'],
# 	['藍','藍'],
# 	['白','白'],
# 	['黑','黑'],
# 	]

# 	user_name = forms.CharField(label='你的名字', max_length=10)
# 	user_color = forms.ChoiceField(label='幸運顏色', choices=COLORS)


'''
Datepicker is totally failed to work, but thanks to the link, I inject this widget from jquery
but for the good look of it, I use forms.Form instead of forms.ModelForm
http://www.derricksherrill.com/django/django-date-picker/
'''
class DiaryForm(forms.Form):
	budget = forms.IntegerField(label = '花費')
	weight = forms.IntegerField(label = '體重')
	note = forms.CharField(label = '註記',widget=forms.Textarea)
	# ddate = forms.DateField(label = '日期',widget=forms.DateInput(attrs={'class':'datepicker'}))


'''

class DiaryForm(forms.ModelForm):

	# date = forms.DateField(widget=DatePicker(options={"format":"mm/dd/yy","autoclose":True}))

	class Meta:
		model = models.Diary
		fields = ['budget', 'weight', 'note']
		# widget = {'ddate':forms.DateInput(format=('%d-%m-%Y'),attrs={'class':'datepicker'})}
		# exclude = ['owner', 'active']

	def __init__(self, *args, **kwargs):
		super(DiaryForm, self).__init__(*args, **kwargs)
		self.fields['budget'].label = '今日花費 (元)'
		self.fields['weight'].label = '今日體重 (KG)'
		self.fields['note'].label = '寫些東西？'
		# self.fields['ddate'].label = '日期'
		# self.fields['ddate'].widget = DatePicker(options={"format":"mm/dd/yy","autoclose":True})
'''