from django.conf.urls import url
from sbesbank import views

urlpatterns = [
    #region UserUrls
    url(r'^api/sbesbank/loginuser', views.LogInUser),
    url(r'^api/sbesbank/registeruser', views.RegisterUser),

    #endregion

    #region AdminUrls
    # NOTE: for this methods perform credentials check
    url(r'^api/sbesbank/getAccounts',views.GetAllAccountsInBank),
    url(r'^api/sbesbank/blockaccount',views.BlockAccount),

    #endregion

    #region AccountUrls
    url(r'^api/sbesbank/accountinfo', views.AccInfo),
    url(r'^api/sbesbank/transactions', views.AccTransactions),
    url(r'^api/sbesbank/createaccount',views.CreateAccount),

    #endregion
    
    #region CardUrls
    url(r'^api/sbesbank/accountCards',views.AccCards),
    url(r'^api/sbesbank/createNewCard',views.createCardPOST),

    #endregion

    #region TransactionUrls
    url(r'^api/sbesbank/tractransfer/', views.TrAcTransfer),
    url(r'^api/sbesbank/trmyacc/', views.TrMyAcc),
    url(r'^api/sbesbank/createpayment',views.CreatePayment),
    url(r'^api/sbesbank/doTransaction', views.DoTransaction),
    url(r'^api/sbesbank/exchangeMoney',views.ExchangeMoney),
    url(r'^api/sbesbank/checkCurrency',views.CheckCurrency),
    
    #endregion

    #region CurrencyUrls
    url(r'^api/sbesbank/initcurrencies',views.InitCurrencies),

    #endregion

    #region PaymentCodeUrls
    url(r'^api/sbesbank/initpaymentcodes',views.InitPaymentCodes),
    url(r'^api/sbesbank/getpaymentcodes',views.GetPaymentCodes),
    #endregion

    #region CertificateUrls
    url(r'^api/sbesbank/serverpublickey',views.GetServerPublicKey),
    url(r'^api/sbesbank/userpublickey',views.GetUserPublicKey),
    url(r'^api/sbesbank/userpivatekey',views.GetUserPrivateKey),


    #endregion
]
