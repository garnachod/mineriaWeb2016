from django.http import HttpResponse
from django.core.paginator import Paginator
from django.template import loader
from django.shortcuts import render, redirect
from .models import Tarea
from API.APISentimientos import APISentimientos
from collections import namedtuple
import datetime
import json
import calendar


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
	if len (request.GET['search']) < 2 or len(request.GET['search']) > 16:
		template = loader.get_template('mineria/index.html')
		context = {}
		return HttpResponse(template.render(context, request))
	if 'search' in request.GET and 'lang' in request.GET:
		createTask('SentimentsByMentions', request.GET['search'], request.GET['lang'])
		
	tareas = Tarea.objects.order_by('-inicio')
	Task = namedtuple('Task', 'username, idioma, finished, id')
	tareas_ = []
	finished_count = 0
	no_finished_count = 0
	for tarea in tareas:
		if len(tarea.username.lower()) <2 or len(tarea.username.lower()) > 16:
			Tarea.objects.get(pk=tarea.id).delete()
			continue
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

	count = 0
	act_month = datetime.date.today().month
	act_year = datetime.date.today().year
	array = []

	mes = calendar.month_name[act_month]

	for t in tareas:
		d = t.inicio
		array.append(d)

	content_month = obtainMes(array,act_month)
	content_year = obtainYear(array,act_year)
    
	context = {'tareas' : tareas, 'month': mes,'year': act_year, 'array_month' : content_month,
	'array_year' : content_year}
	
	return render(request, "mineria/statistics.html", context)

def obtainMes(array,act_month):
	cadena = ""
	count = 0 
	count_a = 0
	while count_a<32:
		count_a = count_a + 1
		count = 0
		for day in array:
			if day.month == act_month and count_a == day.day:
				count = count +1
		cadena = cadena + "%d," % count

	return cadena

def obtainYear(array,act_year):
	cadena = ""
	count = 0 
	count_a = 0
	while count_a<13:
		count_a = count_a + 1
		count = 0
		for day in array:
			if day.year == act_year and count_a == day.month:
				count = count +1
		cadena = cadena + "%d," % count

	return cadena
