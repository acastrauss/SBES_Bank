from django.conf.urls import url
from sbesbank import views


urlpatterns = [
    url(r'^api/sbesbank/id=([0-9]*)', views.TrAcTransfer)
]
