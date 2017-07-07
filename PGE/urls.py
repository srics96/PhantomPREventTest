from django.conf.urls import include
from django.conf.urls import url

from PGE.views import add_employee, add_tasks, handle_message 

urlpatterns = [
	url(r'^submitTasks', add_tasks, name = "add_tasks"),
	url(r'^submitMessage', handle_message, name="handle_message"),
	url(r'^addEmployee', add_employee, name="add_employee"),
] 