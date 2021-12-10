from django.conf.urls import url
from sbesbank import views


urlpatterns = [
    url(r'^api/sbesbank/tractransfer/id=([0-9]*)', views.TrAcTransfer),
    url(r'^api/sbesbank/trmyacc/id=([0-9]*)', views.TrMyAcc),
    url(r'^api/sbesbank/accountinfo/id=([0-9]*)', views.AccInfo),
    url(r'^api/sbesbank/transaction/id=([0-9]*)', views.Transact)
]
