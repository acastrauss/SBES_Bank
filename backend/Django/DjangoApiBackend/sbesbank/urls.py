from django.conf.urls import url
from sbesbank import views


urlpatterns = [
    url(r'^api/sbesbank/tractransfer/id=([0-9]*)', views.TrAcTransfer),
    url(r'^api/sbesbank/trmyacc/id=([0-9]*)', views.TrMyAcc),
    url(r'^api/sbesbank/iuser/id=([0-9]*)', views.IUserData),
    url(r'^api/sbesbank/accountinfo/id=([0-9]*)', views.AccInfo),
    url(r'^api/sbesbank/transaction/id=([0-9]*)', views.Transact),
    url(r'^api/sbesbank/client/id=([0-9]*)', views.getClient),
    url(r'^api/sbesbank/certificate/id=([0-9]*)', views.CertData),
    url(r'^api/sbesbank/transactions/accNum=([0-9]*)', views.AccTransactions),
    url(r'^api/sbesbank/user', views.createUser),
    url(r'^api/sbesbank/client', views.createClient),
    url(r'^api/sbesbank/account', views.createAccount),
    url(r'^api/sbesbank/accCli', views.createNewClientAccount),
    url(r'^api/sbesbank/loginuser', views.LogInUser),
]
