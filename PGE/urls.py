from django.conf.urls import include
from django.conf.urls import url

from PGE.views import add_employee, add_tasks, get_employees, handle_message, list_tasks

urlpatterns = [
	url(r'^submitTasks', add_tasks, name = "add_tasks"),
	url(r'^submitMessage', handle_message, name="handle_message"),
	url(r'^addEmployee', add_employee, name="add_employee"),
	url(r'^listTasks', list_tasks, name="list_tasks"),
	url(r'^getEmployees/(?P<role>[A-Z]+)', get_employees, name="get_employees"),
] 