from django.http import HttpResponse
from django.template import loader
from .models import Tarea
import datetime


def getTask(n=10):
	print Tarea.objects.values_list(flat=True)

def createTask(tipo, username, idioma):
	t = Tarea(tipo=tipo, username=username, idioma=idioma, inicio=datetime.datetime.now())
	t.save()


def index(request):
    template = loader.get_template('mineria/index.html')
    context = { }
    #test
    getTask()
    return HttpResponse(template.render(context, request))

def dashboard(request):
    template = loader.get_template('mineria/dashboard.html')
    context = { }
    #test
    getTask()
    return HttpResponse(template.render(context))

def charts(request):
    template = loader.get_template('mineria/charts.html')
    context = { }
    #test
    getTask()
    return HttpResponse(template.render(context))

def tables(request):
    template = loader.get_template('mineria/tables.html')
    context = { }
    #test
    getTask()
    return HttpResponse(template.render(context))