import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-create-payment-form',
  templateUrl: './create-payment-form.component.html',
  styleUrls: ['./create-payment-form.component.css']
})
export class CreatePaymentFormComponent implements OnInit {
  public payment : any;
  public paymentForm : FormGroup;
  public account : AccountModel;
  constructor(private formBuilder : FormBuilder,private transactionService : TransactionService,private router : Router) { 

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
}
