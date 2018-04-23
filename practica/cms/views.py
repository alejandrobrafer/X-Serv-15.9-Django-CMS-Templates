from django.shortcuts import render_to_response

# Create your views here.

from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.csrf import csrf_exempt
from cms.models import Pages

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

def annotated(request, key):
	try:
		resource = Pages.objects.get(name=key)
		return render_to_response('plantilla.html', {'text': resource.page})
	except Pages.DoesNotExist:
		return HttpResponseNotFound('<h1><center>Resource not found</center></h1>')
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
