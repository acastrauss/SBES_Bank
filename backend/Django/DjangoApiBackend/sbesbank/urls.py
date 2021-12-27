from django.conf.urls import url
from sbesbank import views

urlpatterns = [
    url(r'^api/sbesbank/tractransfer/id=([0-9]*)', views.TrAcTransfer),
    url(r'^api/sbesbank/trmyacc/', views.TrMyAcc),
    url(r'^api/sbesbank/iuser/id=([0-9]*)', views.IUserData),
    url(r'^api/sbesbank/accountinfo', views.AccInfo),
    url(r'^api/sbesbank/changeacc/clientId=([0-9]*)&currency=([a-zA-Z]{2,})', views.ChangeAccount),
    # url(r'^api/sbesbank/createacc/clientId=([0-9]*)&currency=([a-zA-Z]{2,})', views.createAccountPOST),
    url(r'^api/sbesbank/transaction/id=([0-9]*)', views.Transact),
    url(r'^api/sbesbank/client/id=([0-9]*)', views.getClient),
    url(r'^api/sbesbank/certificate/id=([0-9]*)', views.CertData),
    url(r'^api/sbesbank/transactions', views.AccTransactions),
    url(r'^api/sbesbank/user', views.createUser),
    url(r'^api/sbesbank/client', views.createClient),
    # url(r'^api/sbesbank/account', views.createAccount),
    url(r'^api/sbesbank/accCli', views.createNewClientAccount),
    url(r'^api/sbesbank/loginuser', views.LogInUser),
    url(r'^api/sbesbank/registeruser', views.RegisterUser),
    url(r'^api/sbesbank/addTransaction', views.AddTransaction),
    url(r'^api/sbesbank/initcurrencies',views.InitCurrencies),
    url(r'^api/sbesbank/createNewCard',views.createCardPOST),
    url(r'^api/sbesbank/accountCards',views.AccCards),
    url(r'^api/sbesbank/doTransaction', views.DoTransaction),
    url(r'^api/sbesbank/checkCurrency',views.CheckCurrency),
    url(r'^api/sbesbank/exchangeMoney',views.ExchangeMoney),
    url(r'^api/sbesbank/getAccounts',views.GetAllAccountsInBank),
    url(r'^api/sbesbank/blockaccount',views.BlockAccount),
    url(r'^api/sbesbank/createpayment',views.CreatePayment),
    url(r'^api/sbesbank/createaccount',views.CreateAccount)
]
