from django.db import models

class Researcher(models.Model):
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)

class Department(models.Model):
	acronym = models.CharField(max_length=10)
	description = models.CharField(max_length=255)
	email = models.EmailField()
	contact_number = models.CharField(max_length=255)

class FacultyReg(models.Model):
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	add_date = models.DateTimeField(auto_now_add=True)

class FacultyProfile(models.Model):
	id = models.ForeignKey(FacultyReg, primary_key=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	middle_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)

class Tag(models.Model):
	name = models.CharField(max_length=255)

class Category(models.Model):
	name = models.CharField(max_length=255)

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

class Tags_Added(models.Model):
	tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
	thesis = models.ForeignKey(Thesis)
	add_date = models.DateTimeField(auto_now_add=True)

class Categories_Added(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	thesis = models.ForeignKey(Thesis)
	add_date = models.DateTimeField(auto_now_add=True)