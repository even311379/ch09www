from django.db import models
from django.contrib.auth.models import User as dUser

# Create your models here.
class Mood(models.Model):
	status = models.CharField(max_length=10,null=False)

	def __str__(self):
		return self.status

class Post(models.Model):
	mood = models.ForeignKey('Mood', on_delete=models.CASCADE)
	nickname = models.CharField(max_length=10, default='遊蕩怪物')
	message = models.TextField(null=False)
	del_pass = models.CharField(max_length=10)
	pub_time = models.DateTimeField(auto_now=True)
	enabled = models.BooleanField(default=False)

	def __str__(self):
		return self.message


class User(models.Model):
	name = models.CharField(max_length = 20, null=False)
	email = models.EmailField(blank=True)
	password = models.CharField(max_length = 20, null=False)
	enabled = models.BooleanField(default = False)

	def __str__(self):
		return self.name

class Profile(models.Model):
	user = models.OneToOneField(dUser, on_delete=models.CASCADE)
	height = models.PositiveIntegerField(default = 180)
	male = models.BooleanField(default=False)
	website = models.URLField(null=True,blank=True)
	description = models.TextField(null=True,blank=True)

	def __str__(self):
		return self.user.username


class Diary(models.Model):
	user = models.ForeignKey(dUser, on_delete=models.CASCADE)
	budget = models.FloatField(default=0)
	weight = models.FloatField(default=0)
	note = models.TextField(blank=True)
	ddate = models.DateField(blank=False)

	def __str__(self):
		return "{0} ({1})".format(self.ddate, self.user)