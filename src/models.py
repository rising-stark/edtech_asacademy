from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Profiles(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	phone = models.IntegerField(blank=True, null=True)
	email = models.EmailField(max_length=254, blank=True, null=True)
	address = models.CharField(max_length=200, blank=True, null=True)
	dob = models.DateTimeField(blank=True, null=True)
	created_at = models.DateTimeField(default=now)

class Teachers(models.Model):
	teacher = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Parents(models.Model):
	parent = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Students(models.Model):
	student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	parent = models.ForeignKey(Parents, on_delete=models.CASCADE, blank=True, null=True)

class Courses(models.Model):
	course_id = models.AutoField(primary_key=True)
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=200)
	course_starts_at = models.DateTimeField(default=now)
	course_ends_at = models.DateTimeField(blank=True, null=True)
	course_price = models.IntegerField(default=0)
	price_id = models.CharField(max_length=200, blank=True, null=True)

# class Plans(models.Model):
# 	plan_id = models.AutoField(primary_key=True)
# 	plan_name = models.CharField(max_length=200)
# 	plan_price = models.IntegerField(default=0)
# 	plan_starts_at = models.DateTimeField(default=now)
# 	plan_ends_at = models.DateTimeField(blank=True, null=True)
# 	courses = models.ManyToManyField(Courses)

class Teaches(models.Model):
	teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)

# class Enrollments(models.Model):
# 	enrollment_id = models.AutoField(primary_key=True)
# 	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
# 	plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE)

class Takes(models.Model):
	student = models.ForeignKey(Students, on_delete=models.CASCADE)
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)

class Lessons(models.Model):
	lesson_id = models.AutoField(primary_key=True)
	course = models.ForeignKey(Courses, on_delete=models.CASCADE)
	lesson_taken_by = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	lesson_link = models.CharField(max_length=200)
	lesson_starts_at = models.DateTimeField(default=now)
	lesson_ends_at = models.DateTimeField(blank=True, null=True)