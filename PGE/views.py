from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

import json

# Utility method to delete unicodes

TASK_ADDITION_KEY_PROJECT_NAME = "project_name"
TASK_ADDITION_KEY_TASKS = "tasks"

def byteify(input):
    if isinstance(input, dict):
        return {byteify(key): byteify(value)
                for key, value in input.items()}
    elif isinstance(input, list):
        return [byteify(element) for element in input]
    elif isinstance(input, bytes):
        return input.encode('utf-8')
    else:
        return input
@csrf_exempt
def add_tasks(request):
    if request.method == 'POST':
        recieved_json = json.loads(request.body)
        task_dict = byteify(recieved_json)
        for key, value in task_dict.items():
            print (key, value)
        response = {
            "message" : "successfull"
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        response = {
            "message" : "Forbidden"
        }
        return HttpResponse(json.dumps(response), content_type="application/json")
@csrf_exempt
def handle_message(request):
    if request.method == 'GET':
        return HttpResponse(data)



