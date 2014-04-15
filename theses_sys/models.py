from django.db import models

class Researcher(models.Model):
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.last_name + ', ' + self.first_name + ' ' + self.middle_name[0] + '.'

class Department(models.Model):
	name = models.CharField(max_length=255)
	email = models.EmailField()
	contact_number = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name

class FacultySession(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	date_joined = models.DateTimeField(auto_now_add=True)
	date_last_login = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return self.username

class FacultyProfile(models.Model):
	user_auth = models.ForeignKey(FacultySession, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	gender = models.CharField(max_length=1)
	department = models.ForeignKey(Department)
	email = models.EmailField()
	contact_number = models.CharField(max_length=255)
	def __unicode__(self):
		return self.last_name + ', ' + self.first_name + ' ' + self.middle_name[0] + '.'

class Tag(models.Model):
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=255)
	def __unicode__(self):
		return self.name

class Thesis(models.Model):
	title = models.CharField(max_length=255)
	abstract = models.TextField()
	researchers = models.ManyToManyField(Researcher)
	faculty = models.ForeignKey(FacultyProfile, on_delete=models.CASCADE)
	tags = models.ManyToManyField(Tag, through='Tags_Added')
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	date_last_modified = models.DateTimeField(auto_now=True)
	add_date = models.DateTimeField(auto_now_add=True)
	pub_date = models.DateTimeField()
	acc_date = models.DateTimeField()
	def __unicode__(self):
		return self.title

class Tags_Added(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
	add_date = models.DateTimeField(auto_now_add=True)