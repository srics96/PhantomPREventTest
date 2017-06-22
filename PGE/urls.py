from django.conf.urls import include
from django.conf.urls import url

from PGE.views import handle_message 

urlpatterns = [
	url(r'^submitMessage', handle_message, name="handle_message"),
]