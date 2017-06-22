from django.shortcuts import render
from django.http import HttpResponse


def handle_message(request):
	if request.method == 'GET':
		return HttpResponse(data)


