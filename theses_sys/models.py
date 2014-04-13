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

class FacultyReg(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	add_date = models.DateTimeField(auto_now_add=True)
	def __unicode__(self):
		return self.name

class FacultyProfile(models.Model):
	id = models.ForeignKey(FacultyReg, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	department = models.ForeignKey(Department)
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
	categories = models.ManyToManyField(Category, through='Categories_Added')
	add_date = models.DateTimeField(auto_now_add=True)
	pub_date = models.DateTimeField()
	acc_date = models.DateTimeField()
	def __unicode__(self):
		return self.title

class Tags_Added(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
	add_date = models.DateTimeField(auto_now_add=True)

class Categories_Added(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	thesis = models.ForeignKey(Thesis, on_delete=models.CASCADE)
	add_date = models.DateTimeField(auto_now_add=True)