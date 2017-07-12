from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PGE.models import Employee, Manager, Priority, Project, Role, Task
from PGE.serializers import EmployeeSerializer

from datetime import datetime, timedelta


from dateutil import parser

import json
import pyrebase
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


config = {
  "apiKey": "AIzaSyB4555K4PmN7z5oMFIIfu08HSV_NRReSZQ",
  "authDomain": "phantom-gab-engine.firebaseapp.com",
  "databaseURL": "https://phantom-gab-engine.firebaseio.com",
  "storageBucket": "phantom-gab-engine.appspot.com",
  "serviceAccount": "PGE/phantom-gab-engine-firebase-adminsdk-o9tcv-6faea27d58.json"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("sriablaze@gmail.com", "1234sri#")
db = firebase.database()

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
RESULT_KEY = "result"
DATE_DEADLINE_KEY = "date_deadline"
DURATION_DEADLINE_KEY = "duration_deadline"
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
        selection_dict = {}
        tasks = []
        recieved_json = json.loads(request.body)
        recieved_dict = byteify(recieved_json)
        channel_name = recieved_dict['channel_name']
        manager_email = recieved_json['manager_email']
        

        employee_obj = Employee.objects.get(email=manager_email)
        Manager.objects.all().delete()
        manager_obj, created = Manager.objects.get_or_create(employee_instance=employee_obj)
        project_obj = Project(project_name=channel_name, manager=manager_obj)
        project_obj.save()
        for task_obj in recieved_dict['tasks']:
            tasks.append(task_obj)
        for role_emp_object in recieved_dict["employees"]:
            role_name = role_emp_object['role_name']
            employee_email = role_emp_object['employee']['email']
            role_obj = Role.objects.get(role_name=role_name)
            employee = Employee.objects.get(email=email)
            selection_obj, created = Selection.objects.get_or_create(role=role_obj)
            selection_obj.employees.add(employee)
            selection_dict[role_name] = selection_obj

        print(selection_dict)
        for role, selection_obj in selection_dict.items():
            project_obj.selections.add(selection_obj)

        request_list = []
        entity_entries = [] 
        entity_name = TASK_ENTITY_NAME
        
        
        for task in tasks:
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
        message = message.replace("@", "")
        print(message)
        headers['Authorization'] = 'Bearer {0}'.format(CLIENT_ACCESS_TOKEN)
        request_dict = {"query" : [message], "sessionId" : SESSION_ID, "lang" : "en" } 
        request_dict = json.dumps(request_dict)
        response = requests.post(MESSAGE_SUBMISSION_URL, data=request_dict, headers=headers)
        response_dict = byteify(response.json())
        results_dict = response_dict[RESULT_KEY]
        action_incomplete = results_dict[ACTION_INCOMPLETE]
        if action_incomplete is False:
            result_parameters = results_dict["parameters"]
            employees = result_parameters["employee"]
            print (employees)
            task = result_parameters["task"]
            print (task)
            deadline_dict = result_parameters["deadline"]
            date_duration = deadline_dict.get(DATE_DEADLINE_KEY, None)
            duration_deadline = deadline_dict.get(DURATION_DEADLINE_KEY, None)
            if duration_deadline is not None:
                amount = duration_deadline["amount"]
                unit = duration_deadline["unit"]
                if unit == "day":
                    deadline = datetime.date().now() + timedelta(days=int(amount))
            else:
                deadline = parser.parse(date_duration)
            print(deadline)

        fulfillment = results_dict['fulfillment']   
        speech_response = fulfillment['speech']
        response = {
            "speech_response" : speech_response
        }
        
        return HttpResponse(json.dumps(response), content_type="application/json")
    
    elif request.method == 'GET': 
        return HttpResponse(status=403)


@csrf_exempt
def get_employees(request, role='WFD'):
    if request.method == 'GET':
        print(role)
        queryset = Employee.objects.filter(priority__role__role_name=role).order_by('priority__magnitude', 'name')
        employee_serializer = EmployeeSerializer(queryset, many=True)
        print(employee_serializer.data)
        return JsonResponse(employee_serializer.data, status=201, safe=False)


@csrf_exempt
def add_employee(request):
    if request.method == 'POST':
        roles = []
        role_keys = ["1", "2", "3"]
        recieved_json = json.loads(request.body)
        recieved_dict = byteify(recieved_json)
        name = recieved_dict["name"]
        email = recieved_dict["email"]
        for priorities in role_keys:
            roles.append(recieved_dict.get(priorities, None))
        print(roles)
        for (index, role) in enumerate(roles):
            if role is not None:
                role_obj = Role.objects.get(role_name=role)
                priority_obj = Priority.objects.get(role=role_obj, magnitude=index + 1)
                employee_obj = Employee(name=name, email=email)
                employee_obj.save()
                employee_obj.priority.add(priority_obj)
        return HttpResponse(status=200)


                



    '''
    employee = Employee.objects.get(email="skandyruban@gmail.com")
    input_dict = {"name": "Rithwin Siva", "email": "rithwinsiva@gmail.com"}
    db.child("employees").push(input_dict, user['idToken'])
    '''

    
        



        



