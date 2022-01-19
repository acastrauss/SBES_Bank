import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { TransactionService } from '../services/transaction.service';
import {JSEncrypt} from 'jsencrypt';

@Component({
  selector: 'app-create-payment-form',
  templateUrl: './create-payment-form.component.html',
  styleUrls: ['./create-payment-form.component.css']
})
export class CreatePaymentFormComponent implements OnInit {
  public payment : any;
  public paymentForm : FormGroup;
  public account : AccountModel;
  private publicKey : string;
  private dataString : string;
  constructor(private formBuilder : FormBuilder,private transactionService : TransactionService,private router : Router) { 


    this.publicKey = JSON.parse(localStorage.getItem('sertificate')!); 

    this.account = JSON.parse(localStorage.getItem('account')!);
    this.paymentForm = this.formBuilder.group({
      accNum :[''],
      amount :['',[Validators.required]]
    });
  }

  ngOnInit(): void {
  }

  public get amount() {
    return this.paymentForm.get('amount') ;
  }

  public submitForm(data : any){
    
    console.log(data);
    this.dataString = JSON.stringify(data);

    data = this.encryptWithPublicKey(this.dataString);
    console.log(data)
    if(!this.paymentForm.valid){
      window.alert('Not valid!');
      return;
    }
    
    this.transactionService.createPayment(data).subscribe((pay : any)=>{
        this.payment = pay;
        console.log(this.payment);
        this.router.navigate(['/account',this.account.accountNumber]);
        alert("Uspjesna uplata!");
        this.paymentForm.reset();
    });
  }
  
  public encryptWithPublicKey(valueToEncrypt: any): string {
    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(this.publicKey);
    return encrypt.encrypt(String(valueToEncrypt));
  }
}
