from django.db import models
from django.conf import settings
from django.utils.timezone import now

class Profiles(models.Model):
	user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, null=True)
	last_name = models.CharField(max_length=200, null=True)
	phone = models.IntegerField(null=True)
	email = models.EmailField(max_length=254, null=True)
	address = models.CharField(max_length=200, null=True)
	dob = models.DateTimeField(null=True)
	created_at = models.DateTimeField(default=now)


class Admins(models.Model):
	admin_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Teachers(models.Model):
	teacher_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Parents(models.Model):
	parent_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Students(models.Model):
	student_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class Subjects(models.Model):
	subject_id = models.AutoField(primary_key=True)
	subject_name = models.CharField(max_length=200)

class Plans(models.Model):
	plan_id = models.AutoField(primary_key=True)
	plan_name = models.CharField(max_length=200)
	plan_price = models.IntegerField(default=0)
	plan_starts_at = models.DateTimeField(default=now)
	plan_ends_at = models.DateTimeField(null=True)

class Courses(models.Model):
	course_id = models.AutoField(primary_key=True)
	subject_id = models.ForeignKey(Subjects, on_delete=models.CASCADE)
	plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE, blank=True, null=True)
	course_code = models.CharField(max_length=10)
	course_name = models.CharField(max_length=200)
	course_starts_at = models.DateTimeField(default=now)
	course_ends_at = models.DateTimeField(null=True)
	course_price = models.IntegerField(default=0)

class Teaches(models.Model):
	teacher_id = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)

class Enrollments(models.Model):
	enrollment_id = models.AutoField(primary_key=True)
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	plan_id = models.ForeignKey(Plans, on_delete=models.CASCADE)

class Takes(models.Model):
	student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
	course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)


class Lessons(models.Model):
	lesson_id = models.AutoField(primary_key=True)
	course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
	lesson_taken_by = models.ForeignKey(Teachers, on_delete=models.CASCADE)
	lesson_link = models.CharField(max_length=200)
	lesson_starts_at = models.DateTimeField(default=now)
	lesson_ends_at = models.DateTimeField(null=True)