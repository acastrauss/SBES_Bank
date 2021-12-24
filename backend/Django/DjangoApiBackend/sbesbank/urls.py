from django.conf.urls import url
from sbesbank import views

urlpatterns = [
    url(r'^api/sbesbank/tractransfer/id=([0-9]*)', views.TrAcTransfer),
    url(r'^api/sbesbank/trmyacc/', views.TrMyAcc),
    url(r'^api/sbesbank/iuser/id=([0-9]*)', views.IUserData),
<<<<<<< HEAD
    url(r'^api/sbesbank/accountinfo/', views.AccInfo),
=======
    url(r'^api/sbesbank/accountinfo/id=([0-9]*)', views.AccInfo),
    url(r'^api/sbesbank/changeacc/clientId=([0-9]*)&currency=([a-zA-Z]{2,})', views.ChangeAccount),
    url(r'^api/sbesbank/createacc/clientId=([0-9]*)&currency=([a-zA-Z]{2,})', views.createAccountPOST),
>>>>>>> 49a168748992e232e74ba5fbba7fb22372b30339
    url(r'^api/sbesbank/transaction/id=([0-9]*)', views.Transact),
    url(r'^api/sbesbank/client/id=([0-9]*)', views.getClient),
    url(r'^api/sbesbank/certificate/id=([0-9]*)', views.CertData),
    url(r'^api/sbesbank/transactions/accNum=([0-9]*)', views.AccTransactions),
    url(r'^api/sbesbank/user', views.createUser),
    url(r'^api/sbesbank/client', views.createClient),
    url(r'^api/sbesbank/account', views.createAccount),
    url(r'^api/sbesbank/accCli', views.createNewClientAccount),
    url(r'^api/sbesbank/loginuser', views.LogInUser),
    url(r'^api/sbesbank/registeruser', views.RegisterUser),
    url(r'^api/sbesbank/addTransaction', views.AddTransaction),
    url(r'^api/sbesbank/initcurrencies',views.InitCurrencies)
]
