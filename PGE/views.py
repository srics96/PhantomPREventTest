from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PGE.models import Employee, Manager, Project, Role, Task

import json
import os.path
import sys
import requests


try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

CLIENT_ACCESS_TOKEN = '75d2f175cd05473fbddba4d6475a49d8'
SESSION_ID = 1001

# Utility method to delete unicodes

TASK_ADDITION_KEY_PROJECT_NAME = "project_name"
TASK_ADDITION_KEY_TASKS = "tasks"
TASK_ADDITION_MANAGER_EMAIL = "manager_email"
TASK_ENTITY_NAME = "Task"
TASK_ENTITY_ADDITION_URL = "https://api.api.ai/v1/entities/{0}/entries?v=20150910".format(TASK_ENTITY_NAME)
MESSAGE_SUBMISSION_URL = "https://api.api.ai/v1/query?v=20150910"
SUCCESS_STATUS_CODE = 200
MESSAGE_REQUEST_KEY = "message"
ACTION_INCOMPLETE = "actionIncomplete"
headers = {'Content-Type': 'application/json; charset=utf-8', 'Authorization': 'Bearer b55df5347afe4002a39e94cd61c121c9'}


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


def call_api(session_id, query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

    request = ai.text_request()

    request.session_id = session_id

    request.query = query

    response = request.getresponse()

    return response.read()


@csrf_exempt
def add_tasks(request):
    if request.method == 'POST':
        request_list = []
        entity_entries = []
        entity_name = TASK_ENTITY_NAME
        recieved_json = json.loads(request.body)
        input_dict = byteify(recieved_json)
        manager_email = input_dict[TASK_ADDITION_MANAGER_EMAIL]
        employee_obj = Employee.objects.get(email=manager_email)
        manager_obj, created = Manager.objects.get_or_create(employee_instance=employee_obj)
        project_name = input_dict[TASK_ADDITION_KEY_PROJECT_NAME]
        project_obj = Project(project_name=project_name, manager=manager_obj)
        project_obj.save()
        task_names = input_dict[TASK_ADDITION_KEY_TASKS]
        for task in task_names:
            task_obj = Task(task_name=task, project=project_obj)
            task_obj.save()
            task_name = task_obj.task_name
            request_dict = {"value" : task_obj.task_name, "synonyms" : [task_name]}
            request_list.append(request_dict)
        request_list = json.dumps(request_list)
        entity_request = requests.post(TASK_ENTITY_ADDITION_URL, data=request_list, headers=headers)
        if entity_request.status_code == SUCCESS_STATUS_CODE:
            print("Entity added successfully")
            return HttpResponse(status=200)
        else:
            return HttpResponse(status=500)
    else:
        return HttpResponse(status=403)


@csrf_exempt
def handle_message(request):
    if request.method == 'POST':
        recieved_json = json.loads(request.body)
        input_dict = byteify(recieved_json)
        message = input_dict[MESSAGE_REQUEST_KEY]
        message = message.lstrip()
        message = message[8:]
        headers['Authorization'] = 'Bearer {0}'.format(CLIENT_ACCESS_TOKEN)
        request_dict = {"query" : [message], "sessionId" : SESSION_ID, "lang" : "en" } 
        request_dict = json.dumps(request_dict)
        response = requests.post(MESSAGE_SUBMISSION_URL, data=request_dict, headers=headers)
        response_dict = byteify(response.json())
        print(response_dict)
        print(results_dict)
    
    elif request.method == 'GET': 
        response = send_query("Hi")
        response_dict = byteify(response)
        return HttpResponse(response_dict)

        



