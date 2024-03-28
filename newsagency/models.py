from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class Login(models.Model):
	user = models.ForeignKey(User, on_delete = models.CASCADE)
	password = models.CharField(max_length = 64)
	
	def __str__(self):
		return self.user.username

class Story(models.Model):
	headline = models.CharField(max_length = 64)
	categories = [('pol', 'Politics'), ('art', 'Art'), ('tech', 'Technology New'), ('trivia', 'Trivial News')]
	story_category = models.CharField(max_length = 64, choices=categories)
	regions = [('uk', 'UK'), ('eu', 'EU'), ('w', 'World News')]
	story_region = models.CharField(max_length = 64, choices=regions)
	story_details = models.CharField(max_length = 128)
	author = models.CharField(max_length = 64, default='')
	story_date = models.CharField(max_length = 64, default=date.today())

	def __str__(self):
		return self.headline
	
class Author(models.Model):
	name = models.CharField(max_length=64, default='')
	username = models.ForeignKey(User, on_delete = models.CASCADE)
	password = models.CharField(max_length = 64, default='')

	def __str__(self):
		return self.name
	
