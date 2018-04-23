from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from cms.models import Pages
from django.template.loader import get_template
from django.template import Context

def principal(request):
	
	resources = Pages.objects.all()
	response = ""
	for resource in resources:
		response += resource.name + "<br>"
	
	if request.user.is_authenticated():
		logged = 'Logged in as ' + request.user.username + '.<br><a href="/admin/logout/">Logout</a><br><br>'
		return HttpResponse(logged + response)
		
	else:
		logged = 'Not logged in.' + '<br><a href="/login">Login</a><br><br>' 
		return HttpResponse(logged + response)

def redirection(request):		
	return HttpResponse("<html>" + "<head><META HTTP-EQUIV='REFRESH' CONTENT='1;URL=//localhost:8000/'>" +
			"</head><body>Redirecting in 1 seconds ...</body></html>")


def annotated(request, key):
	print("aqui")
	template = get_template("Invention/index.html")
	c = Context({'content': key})
	renderizado = template.render(c)
	return HttpResponse(renderizado)
	
@csrf_exempt
def content(request, key):
	
	if request.user.is_authenticated():
		try:
			resource = Pages.objects.get(name=key)
			if request.method == 'PUT':
				updated = Pages(id=resource.id, name=resource.name, page=request.body) 
				updated.save()
				resource.page = request.body
			return HttpResponse(resource.page)
	
		except Pages.DoesNotExist:
			if request.method == 'PUT':
				new = Pages(name=key, page=request.body) 
				new.save()
				return HttpResponse(new.page)
			return HttpResponseNotFound('<h1><center>Resource not found</center></h1>')
	else:
		try:
			resource = Pages.objects.get(name=key)
			return HttpResponse(resource.page + '<br><br>Not logged in.' + '<br><a href="/login">Login</a><br><br>')
		
		except Pages.DoesNotExist:
			return HttpResponse('Resource not found. Not logged in.' + '<br><a href="/login">Login</a><br><br>')
