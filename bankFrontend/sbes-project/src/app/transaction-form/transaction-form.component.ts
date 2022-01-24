import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { AccountModel } from '../models/account.model';
import { AccTransactionsModel } from '../models/accTransactions.model';
import { CardModel } from '../models/card.model';
import { MyAccInfoFKModel } from '../models/myAccInfoFK.model';
import { PaymentCodeFKModel } from '../models/paymentCodeFK.model';
import { TransferAccInfoFKModel } from '../models/transferAccInfoFK.model';
import { TransactionService } from '../services/transaction.service';

import * as CryptoJS from 'crypto-js';
import {JSEncrypt} from 'jsencrypt';
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-transaction-form',
  templateUrl: './transaction-form.component.html',
  styleUrls: ['./transaction-form.component.css']
})
export class TransactionFormComponent implements OnInit {
  public privateKey : string;
  private publicKey : string;
  private dataString : string;

  public transactionObject : AccTransactionsModel;
  public transactionForm : FormGroup;
  public account : AccountModel;
  public currency : string;
  public payment : PaymentCodeFKModel[];
  public paymentUrl : string="http://127.0.0.1:8000/api/sbesbank/getpaymentcodes";
  public json : any;
  public json2: any;
  public paymentCode  : PaymentCodeFKModel[];
  public paymentCodeDesc : PaymentCodeFKModel;
  public cardsAccount : CardModel[] = [];
  constructor(private formBuilder : FormBuilder,private TransService : TransactionService,private router: Router,private http : HttpClient) {
    this.getPayments();
    this.paymentCode = JSON.parse(localStorage.getItem('paymentPurpose')!);
    this.publicKey = JSON.parse(localStorage.getItem('sertificate')!); 
    this.privateKey = JSON.parse(localStorage.getItem('privateSert')!);
    this.transactionForm = this.formBuilder.group({
      cards : ['',Validators.required],
      pin:['',Validators.required],
      cvc:['',Validators.required],
      accountTo:['',[Validators.required]],
      accountToName:['',[Validators.required]],
      accountToBillingAdress:['',[Validators.required]],
      modelCode:['',[Validators.required]],
      description:['',[Validators.required]],
      paymentPurpose:['',[Validators.required]],
      amount:['',[Validators.required]],
      referenceNumber:['',[Validators.required]]
    })
    this.account= JSON.parse(localStorage.getItem('account')!);
    this.cardsAccount = JSON.parse(localStorage.getItem('cardsAccount')!);
    this.transactionObject = <AccTransactionsModel>{};
    this.transactionObject.transferAccInfoFK = <TransferAccInfoFKModel>{};        //initialize
    this.transactionObject.myAccInfoFK = <MyAccInfoFKModel>{};
    this.transactionObject.paymentCodeFK = <PaymentCodeFKModel>{};
  }

  ngOnInit(): void {
  }


  public get cards(){
    return this.transactionForm.get('cards');
  }

  public get pin(){
    return this.transactionForm.get('pin');
  }

  public get cvc(){
    return this.transactionForm.get('cvc');
  }

  public get accountTo() {
    return this.transactionForm.get('accountTo');
  }

  public get accountToName() {
    return this.transactionForm.get('accountToName') ;
  }

  public get accountToBillingAdress() {
    return this.transactionForm.get('accountToBillingAdress');
  }

  public get modelCode() {
    return this.transactionForm.get('modelCode') ;
  }

  public get description() {
    return this.transactionForm.get('description') ;
  }

  public get paymentPurpose() {
    return this.transactionForm.get('paymentPurpose');
  }

  public get amount() {
    return this.transactionForm.get('amount') ;
  }

  public get referenceNumber() {
    return this.transactionForm.get('referenceNumber') ;
  }

  public submitForm(data : any){

    this.transactionObject.amount = data.amount;
    this.transactionObject.modelCode=data.modelCode;


    this.transactionObject.paymentCodeFK.code = data.code;

    this.paymentCodeDesc = this.paymentCode.filter((pay : PaymentCodeFKModel)=>pay.description === data.description)[0];
    this.transactionObject.paymentCodeFK.code = this.paymentCodeDesc.code;
    this.transactionObject.paymentCodeFK.description = data.description;
    this.transactionObject.paymentPurpose= data.paymentPurpose;
    this.transactionObject.referenceNumber=data.referenceNumber;
    this.transactionObject.provision = 0.01;
    this.transactionObject.currency = this.account.currency;
    this.transactionObject.myAccInfoFK.id=this.account.id;
    this.transactionObject.myAccInfoFK.balanceBefore=this.account.accountBalance;
    this.transactionObject.myAccInfoFK.balanceAfter= (this.account.accountBalance-data.amount-this.transactionObject.provision*data.amount);
    this.transactionObject.transactionType = "OUTFLOW";
    this.transactionObject.myAccInfoFK.accountNumber=this.account.accountNumber;
    this.transactionObject.myAccInfoFK.billingAddress=this.account.clientId.userId.billingAddress;
    this.transactionObject.myAccInfoFK.fullName=this.account.clientId.userId.fullName;

    this.transactionObject.transferAccInfoFK.accountNumber = data.accountTo;
    this.transactionObject.transferAccInfoFK.fullName = data.accountToName;
    this.transactionObject.transferAccInfoFK.billingAddress = data.accountToBillingAdress;
    
    console.log(this.transactionObject);

    if(!this.transactionForm.valid){
      window.alert('Not valid!');
      return;
    }
  
    this.transactionObject.cardNumber = data['cards'];
    data['pin']= CryptoJS.SHA256(String(data['pin'])).toString();
    data['cvc']= CryptoJS.SHA256(String(data['cvc'])).toString();
    this.transactionObject.pin =  data['pin'];
    this.transactionObject.cvc =  data['cvc']; 
    
    this.authenticate(this.transactionObject, data);
  }

  
  public encryptWithPublicKey(valueToEncrypt: any): string {

    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(this.publicKey);
    return encrypt.encrypt(String(valueToEncrypt));
  }

  public getPayments():PaymentCodeFKModel[]{
      this.http.get<PaymentCodeFKModel[]>(this.paymentUrl).subscribe((payments : PaymentCodeFKModel[])=>{
        this.payment=payments;
        localStorage.setItem('paymentPurpose',JSON.stringify(this.payment));
        
      console.log(this.payment)
      });
  return this.payment;
}



  public authenticate(transaction : AccTransactionsModel, data:any){
 
    this.TransService.checkCurrency(this.transactionObject.transferAccInfoFK.accountNumber).subscribe((curr : any)=>{
      transaction.currency = curr['Currency'];
    }); 
    
    if(this.account.accountBalance < transaction.amount + transaction.amount* transaction.provision){
      return window.alert('Nemate dovoljno sredstava da izvrsite transakciju!');
    }
    else if (transaction.currency !== this.account.currency)
    {
      return window.alert('Racun na koji zelite da posaljete novac nije u vasoj valuti');
    }else{
      //this.users.push(data);///mozda cu morati data kastovati 
      //localStorage.setItem('users', JSON.stringify(this.users));   
      // ne vodim trenutno racuna o transakcijama
      
      transaction.pin=this.transactionObject.pin;
      transaction.cvc= this.transactionObject.cvc;
      
      this.json = JSON.parse(JSON.stringify(transaction));

      for(var i in this.json){

        if(i==="myAccInfoFK"){
          for(var j in this.json[i])
            this.json[i][j]=this.encryptWithPublicKey(this.json[i][j])
        }else if(
          i==="paymentCodeFK"
        ){
          for(var j in this.json[i])
          this.json[i][j]=this.encryptWithPublicKey(this.json[i][j])
        }else if(
          i==="transferAccInfoFK"  
        ){
          for(var j in this.json[i])
          this.json[i][j]=this.encryptWithPublicKey(this.json[i][j])
        }else{
      this.json[i]=this.encryptWithPublicKey(this.json[i]);}
      };

      this.TransService.createTransaction(this.json).subscribe((trans : AccTransactionsModel) =>{

        this.router.navigate(['/account',this.account.accountNumber]);
        this.transactionForm.reset();
        return window.alert('Transakcija uspjesno obavljena!');
        
      });
    }
  }
}
