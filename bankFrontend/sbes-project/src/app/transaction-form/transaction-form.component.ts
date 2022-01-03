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

@Component({
  selector: 'app-transaction-form',
  templateUrl: './transaction-form.component.html',
  styleUrls: ['./transaction-form.component.css']
})
export class TransactionFormComponent implements OnInit {

  public transactionObject : AccTransactionsModel;
  public transactionForm : FormGroup;
  public account : AccountModel;
  public currency : string;
  public cardsAccount : CardModel[] = [];
  constructor(private formBuilder : FormBuilder,private TransService : TransactionService,private router: Router) {
    this.transactionForm = this.formBuilder.group({
      cards : ['',Validators.required],
      pin:['',Validators.required],
      cvc:['',Validators.required],
      accountTo:['',[Validators.required]],
      accountToName:['',[Validators.required]],
      accountToBillingAdress:['',[Validators.required]],
      modelCode:['',[Validators.required]],
      code:['',[Validators.required]],
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

  public get code() {
    return this.transactionForm.get('code');
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

    this.authenticate(this.transactionObject);
  }

  public authenticate(transaction : AccTransactionsModel){
 
    this.TransService.checkCurrency(this.transactionObject.transferAccInfoFK.accountNumber).subscribe((curr : any)=>{
      this.currency = curr['Currency'];
      console.log(this.currency);
    }); 

    if(this.account.accountBalance < transaction.amount + transaction.amount* transaction.provision){
      return window.alert('Nemate dovoljno sredstava da izvrsite transakciju!');
    }
    else if (this.currency !== this.account.currency)
    {
      return window.alert('Racun na koji zelite da posaljete novac nije u vasoj valuti');
    }else{
      //this.users.push(data);///mozda cu morati data kastovati 
      //localStorage.setItem('users', JSON.stringify(this.users));                  // ne vodim trenutno racuna o transakcijama
      this.TransService.createTransaction(transaction).subscribe((trans : AccTransactionsModel) =>{

        this.router.navigate(['/account',this.account.accountNumber]);
        this.transactionForm.reset();
        return window.alert('Transakcija uspjesno obavljena!');
        
      });
    }
  }
}
