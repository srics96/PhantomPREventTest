from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from PGE.models import Employee, Manager, Project, Role, Task
import json

# Utility method to delete unicodes

TASK_ADDITION_KEY_PROJECT_NAME = "project_name"
TASK_ADDITION_KEY_TASKS = "tasks"
TASK_ADDITION_MANAGER_EMAIL = "manager_email"

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



