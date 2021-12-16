from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from src.models import *
from datetime import datetime, timedelta

def home(request):
	return render(request, "index.html")

def index(request):
	return render(request, "index.html")

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

	# If user is already logged in then render the todo task list
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
				return render(request, 'signup.html')

			try:
				# Check if email already exists
				user = User.objects.get(email=email)
			except User.DoesNotExist:
				user = None

			# If email already exists, show appropriate message and redirect to login page
			if user:
				messages.info(request, 'An account with this email aready exists.')
				return render(request, 'signup.html')

			# Create a new user with the given details
			user = User.objects.create_user(username=username, password=password, email=email)
			user.save(); # user created


			# user automatically logged-in
			auth.login(request, user)
			return redirect('index')
		else:
			messages.info(request, 'passwords not matching...')
			return render(request, 'signup.html')

	return render(request, 'signup.html')

def logout(request):
	auth.logout(request)
	return redirect('/')

def tasklist(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your tasks.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	if request.method == "POST":
		list_name = request.POST["list_name"]

		# Create a new task list
		TaskLists.objects.create(list_name=list_name, username=request.user)

	return redirect('task')

def delete_list(request):
	if request.method == "POST":
		list_id = request.POST["list_id"]

		# Delete the selected task list
		TaskLists.objects.get(pk=list_id).delete()
	return redirect('task')

def delete_task(request):
	if request.method == "POST":
		task_id = request.POST["task_id"]

		# Delete the selected task
		Tasks.objects.get(pk=task_id).delete()
	return redirect('task')

def mark_as_completed(request):
	if request.method == "POST":
		task_id = request.POST["task_id"]

		# Retrieving the particular task with the selected task_id from the database
		t = Tasks.objects.get(pk=task_id)
		t.completed = 1
		t.completed_at = datetime.now()
		t.save()
	return redirect('task')

def mark_as_incomplete(request):
	if request.method == "POST":
		task_id = request.POST["task_id"]

		# Retrieving the particular task with the selected task_id from the database
		t = Tasks.objects.get(pk=task_id)
		t.completed = 0
		t.completed_at = None
		t.save()
	return redirect('task')

def task(request):

	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access your tasks.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	if request.method == "POST":
		task_name = request.POST["task_name"]
		task_desc = request.POST.get("task_desc", "")
		list_id = request.POST.get("list_id", "")
		list_name = request.POST.get("list_name",  "")
		priority = request.POST.get("priority", 0)
		date_due = request.POST.get("date_due", datetime.today() + timedelta(days=1))
		completed = request.POST.get("completed", 0)

		# The paramter "list_id" if not passed from the form, then it means that there was no list present since the current "Create new task" section shows all the available task lists
		if not list_id:
			list_id = TaskLists.objects.create(list_name=list_name, username=request.user)
		else:
			list_id = TaskLists.objects.get(list_id=list_id)

		# Creating a new task according to the parameters passed
		Tasks.objects.create(task_name=task_name, task_desc=task_desc, list_id=list_id, username=request.user, priority=priority, date_due=date_due, completed=completed)

	# Retrieving all the tasklists from the database for this particualr user
	task_lists = TaskLists.objects.filter(username=request.user).order_by("list_id")

	# Retrieving the count of tasks in each task list from the database for this particualr user
	task_count = Tasks.objects.filter(username=request.user).values("list_id").order_by("list_id").annotate(count=Count('task_id'))

	# Retrieving all the tasks from the database for this particualr user
	tasks = Tasks.objects.filter(username=request.user)

	# Convert the "task_count" which is an object contaning ResultSets into a native python dictionary as
	# list_id (key) -> count of tasks in this list (value)
	task_count_dict = {}
	for task in task_count:
		task_count_dict[task['list_id']] = task['count']

	# Including the task count in the tasks object for display purposes in task.html (frontend)
	for task_list in task_lists:
		task_list.count = task_count_dict.get(task_list.list_id, 0)

	return render(request, "task.html", {"task_lists" : task_lists, "tasks" : tasks, "task_count":task_count_dict})

def profile(request):
	if not request.user.is_authenticated:
		messages.info(request, 'You need to be logged-in to access profile page.')
		messages.info(request, 'Don\'t have an account yet? Signup now')
		return redirect('login')

	# Creating a Chart class object
	ch = Chart()

	# Retrieving all the tasks from the database for this particualr user
	tasks = Tasks.objects.filter(username=request.user)

	return render(request, 'profile.html', {"pie_graph_div":ch.pie_completed(tasks)})