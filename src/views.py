import json
import stripe
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic import TemplateView
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.db.models import Count
from src.models import *
from django.core import exceptions

stripe.api_key = settings.STRIPE_SECRET_KEY

def index(request):
	return render(request, "index.html")

def planspricing(request):
	return render(request, "planspricing.html")

def about(request):
	return render(request, "about.html")

def contact(request):
	return render(request, "contact.html")

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		# Try to authenticate the user
		user = auth.authenticate(username=username,password=password)

		# If user is authenticated, then login the user and redirect to task page
		if user is not None:
			auth.login(request, user)
			return redirect("index")
		else:
			messages.info(request, 'invalid credentials')
			return render(request, 'login.html')

	# If user is already logged in then render the index page
	if request.user.is_authenticated:
		return redirect('index')

	return render(request, 'login.html')

def signup(request):
	if request.method == 'POST':
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']

		# Check if the password and confirm_password matches. If not, show appropriate error
		if password == confirm_password:
			user = None
			try:
				# Check if user already exists
				user = User.objects.get(username=username)
			except User.DoesNotExist:
				user = None

			# If user already exists, show appropriate message and redirect to login page
			if user:
				messages.info(request, 'Username Taken. Choose a differet username')
				return render(request, 'login.html')

			try:
				# Check if email already exists
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				user = None

			# If email already exists, show appropriate message and redirect to login page
			if user:
				messages.info(request, 'An account with this email aready exists.')
				return render(request, 'login.html')

			# Create a new user with the given details
			user = User.objects.create_user(username=username, password=password, email=email)
			user.save(); # user created

			# Assigning anyone who signs up as a parent
			p = Parents.objects.create(parent=user)
			p.save()

			# user automatically logged-in
			auth.login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'passwords not matching...')
			return render(request, 'login.html')

	return render(request, 'login.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def get_student_details(parent):
	students = None
	if parent:
		# If the logged-in user is a parent, then
		# Retrieving all the courses and children from the database for this particualr user
		students = Students.objects.filter(parent=parent)
		for s in students:
			user = User.objects.get(pk=s.student_id)
			s.profile = Profiles.objects.get(user=user)
			courses = Takes.objects.filter(student=s)
			courses_enrolled = []
			for c in courses:
				courses_enrolled.append(c.course)
			s.courses = courses_enrolled
	return students

def get_children_count(parent):
	return Students.objects.filter(parent=parent).count()

def profile(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access profile page.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')
	try:
		parent = Parents.objects.get(parent=request.user)
	except IndexError:
		messages.info(request, 'You are not a parent.')
		return redirect('index')
	students = get_student_details(parent)
	enrollments = Enrollments.objects.filter(parent_id=parent)
	return render(request, 'profile.html', {"students":students, "enrollments":enrollments})

def addchild(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your profile.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	if request.method == "POST":
		first_name = request.POST.get("first_name", "")
		last_name = request.POST.get("last_name", "")
		dob = request.POST.get("dob",  "")
		try:
			parent = Parents.objects.get(parent=request.user)
		except IndexError:
			messages.info(request, 'You are not a parent.')
			return redirect('index')
		username = request.user.username + "_child_" + str(get_children_count(parent))

		# Create a new user with the given details
		user = User.objects.create_user(username=username, password=request.user.password)
		user.save(); # user created

		# Creating a student with parent linked
		s = Students.objects.create(student=user, parent=parent)
		s.save()

		# Creating a profile of this student
		p = Profiles.objects.create(user=user, first_name=first_name, last_name=last_name, dob=dob)
		p.save()
		return redirect('profile')

	return render(request, "addchild.html")

def booknow(request):
	courses = Courses.objects.all()

	if not request.user.is_authenticated:
		return render(request, "booknow.html", {"courses":courses, "currency": "??"})
	
	try:
		parent = Parents.objects.get(parent=request.user)
	except exceptions.ObjectDoesNotExist:
		# Logged in user is not parent.
		return render(request, "booknow.html", {"courses":courses, "currency": "??"})
	
	children_count = False
	if parent:
		# If the logged-in user is a parent, then
		# this creates a mapping of courses in which the children of this parent are NOT enrolled in as (key, value) = (course_id, list of children NOT enrolled)
		students = Students.objects.filter(parent=parent)
		if students and courses:
			children_count = True
			for c in courses:
				student_list = []
				for s in students:
					t = Takes.objects.filter(student=s, course=c)
					if not t:
						user = User.objects.get(pk=s.student_id)
						s.profile = Profiles.objects.get(user=user)
						student_list.append(s)
				c.students = student_list
	return render(request, "booknow.html", {"courses":courses, "children_count":children_count, "currency": "??"})

def purchase(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your profile.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	buy_type = request.GET.get("buy_type")
	buy_id = request.GET.get("id")
	children = request.GET.get("children")
	if not buy_type or not buy_id:
		redirect('login')
	elif buy_type == "course":
		course = Courses.objects.get(pk=int(buy_id))
		for c in children.split(","):
			child = Students.objects.get(pk=int(c))
			t = Takes.objects.create(student=child, course=course)
			t.save()
	elif buy_type == "plan":
		plan = Plans.objects.get(pk=int(buy_id))
		parent = Parents.objects.get(parent=request.user)
		Enrollments.objects.create(parent_id=parent, plan_id=plan)
	messages.info(request, f'Your {buy_type} is purchased successfully')
	return redirect('profile')

def stripe_payment(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your profile.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	if request.method == "POST":
		buy_type = request.POST.get("buy_type", "")
		price_id = ""
		mode = ""
		quantity = 1
		if not buy_type:
			return redirect('login')
		elif buy_type == "course":
			course_id = int(request.POST.get("course_id", -1))
			children = request.POST.getlist('children')
			if not children:
				messages.info(request, 'You need to select atleast 1 child.')
				return redirect('booknow')
			if course_id == -1:
				return redirect("booknow")

			price_id = Courses.objects.get(pk=course_id).price_id
			mode = "payment"
			quantity = len(children)
			children = ','.join(children)
			success_url = "&children="+str(children)+"&id="+str(course_id)
		elif buy_type == "plan":
			plan_id = int(request.POST.get("plan_id", -1))
			if plan_id == -1:
				return redirect("booknow")
			price_id = Plans.objects.get(pk=plan_id).price_id
			mode = "subscription"
			success_url = "&id="+str(plan_id)

		checkout_session = ""
		YOUR_DOMAIN = 'http://localhost:8000'
		try:
			checkout_session = stripe.checkout.Session.create(
				line_items=[
					{
						# Provide the exact Price ID (for example, pr_1234) of the product you want to sell
						'price': price_id,
						'quantity': quantity,
					},
				],
				mode=mode,
				success_url=YOUR_DOMAIN + '/purchase?buy_type='+ buy_type + success_url,
				cancel_url=YOUR_DOMAIN + '/booknow',
			)
		except Exception as e:
			print("we are in an exception")
			print(e)
			messages.info(request, 'Server error ocurred. Pls try again later')
			return redirect('booknow')
		return redirect(checkout_session.url)
	return redirect('booknow')