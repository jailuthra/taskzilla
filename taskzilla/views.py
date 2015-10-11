from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from .models import Task, Comment, UserProfile

def index(request):
	tasks_list = Task.objects.filter(closed=False)
	context = {'tasks_list' : tasks_list, 'user' : request.user,}
	return render(request, 'taskzilla/index.html', context)

def task_page(request, task_id):
	task = Task.objects.get(pk=task_id)
	context = {'task' : task, 'comments': task.comment_set.all(), 'user' : request.user}

	if request.method == 'POST' and request.user.is_authenticated():
		user = UserProfile.objects.get (user=request.user)
		comment_text = request.POST['text']
		comment = Comment()
		comment.text = comment_text
		comment.task = task
		comment.user = user
		comment.save()
		return HttpResponseRedirect('/tasks/' + str(task_id))

	return render(request, 'taskzilla/task_page.html', context)

def login_page(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		print(user, username, password)
		if user is not None:
			login(request, user)
			return HttpResponseRedirect('/')
		else:
			return render(request, 'taskzilla/login.html')
	return render(request, 'taskzilla/login.html')

def logout_page(request):
	logout (request)
	return HttpResponseRedirect('/')
