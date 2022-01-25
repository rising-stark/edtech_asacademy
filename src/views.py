from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from src.models import *

def index(request):
	return render(request, "index.html")

def booknow(request):
	return render(request, "booknow.html")

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

def profile(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access profile page.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	parent = Parents.objects.filter(parent=request.user)
	students = None
	if parent:
		# If the logged-in user is a parent, then
		# Retrieving all the courses and children from the database for this particualr user
		students = Students.objects.filter(parent=parent[0])
		for s in students:
			user = User.objects.get(pk=s.student_id)
			s.profile = Profiles.objects.get(user=user)
			courses = Takes.objects.filter(student=s)
			courses_enrolled = []
			for c in courses:
				print(c.course)
				courses_enrolled.append(c.course)
			s.courses = courses_enrolled

	return render(request, 'profile.html', {"students":students})

def addchild(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your tasks.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	if request.method == "POST":
		first_name = request.POST.get("first_name", "")
		last_name = request.POST.get("last_name", "")
		dob = request.POST.get("dob",  "")
		
		try:
			parent = Parents.objects.filter(parent=request.user)[0]
		except IndexError:
			messages.info(request, 'You are not a parent.')
			return redirect('profile')
		children = Students.objects.filter(parent=parent)
		username = request.user.username + "_child_" + str(children.count)
		print("username = ", username)

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