from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render, redirect
from .models import Tarea
from API.APISentimientos import APISentimientos
from collections import namedtuple
import datetime
import json


def createTask(tipo, username, idioma):
	try:
		tarea = Tarea.objects.get(username=username.lower(), idioma=idioma, tipo=tipo)
	except Exception, e:
		#si no existe la tarea, lanzar tambien la api
		t = Tarea(tipo=tipo, username=username.lower(), idioma=idioma, inicio=datetime.datetime.now())
		t.save()
		tarea = Tarea.objects.get(username=username.lower(), idioma=idioma, tipo=tipo)
		if tipo == 'SentimentsByMentions':
			APISentimientos.getSentimentsByMentions(tarea.username.lower(), tarea.idioma.lower())


def index(request):

	template = loader.get_template('mineria/index.html')
	context = {}

	return HttpResponse(template.render(context, request))

def dashboard(request):
	if 'search' in request.GET and 'lang' in request.GET:
		createTask('SentimentsByMentions', request.GET['search'], request.GET['lang'])
		
	tareas = Tarea.objects.order_by('-inicio')
	Task = namedtuple('Task', 'username, idioma, finished, id')
	tareas_ = []
	finished_count = 0
	no_finished_count = 0
	for tarea in tareas:
		fin = APISentimientos.isTaskFinished(tarea.username.lower(), tarea.idioma.lower(), tarea.tipo, download=False)
		if fin == False:
			no_finished_count += 1
			tareas_.append(Task(tarea.username, tarea.idioma, False, tarea.id))
		else:
			finished_count += 1
			tareas_.append(Task(tarea.username, tarea.idioma, True, tarea.id))

	context = {'tareas' : tareas_, 'pending' : no_finished_count, 'finished' : finished_count}
	
	return render(request, "mineria/dashboard.html", context)
	#return HttpResponse(tareas)

def task(request):
	if 'id' not in request.GET:
		return redirect("dashboard.html")

	idTarea = request.GET['id']
	tarea = Tarea.objects.get(pk=idTarea)

	retorno = APISentimientos.getSentimentsByMentions(tarea.username.lower(), tarea.idioma.lower())
	if retorno == False:
		return redirect("dashboard.html")

	pos, neg = retorno
	suma = float(pos + neg)
	pos = float(pos) / suma
	neg = float(neg) / suma
	context = {'pos':pos, 'neg':neg}
	return render(request, "mineria/task.html", context)


def statistics(request):


	tareas = Tarea.objects.order_by('-inicio')

	array = []
	for t in tareas:
		array.append(t.inicio)
	

	print "HOLAAAAAAAAAAAA:"
	#array = [1,2,3,4]
	#array = [50, 20, 10, 40, 15, 25]
	print array

	#json_tar = json.dumps(array)
	context = {'tareas' : tareas, 'array' : array}
	
	return render(request, "mineria/statistics.html", context)

