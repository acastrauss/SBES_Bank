import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { AccountService } from '../services/account.service';

@Component({
  selector: 'app-create-account-form',
  templateUrl: './create-account-form.component.html',
  styleUrls: ['./create-account-form.component.css']
})
export class CreateAccountFormComponent implements OnInit {

  public accountForm : FormGroup;
  public account : AccountModel;
  public accountNew : AccountModel;
  public accountPostoji : AccountModel;
  public accounts : AccountModel[];
  constructor(private formBuilder : FormBuilder,private accountService : AccountService,private router : Router) { 
    this.accounts= JSON.parse(localStorage.getItem('userAccounts')!);

    
    this.account = JSON.parse(localStorage.getItem('account')!);
    this.accountForm = this.formBuilder.group({
      clientId : [''],
      clientName : [''],
      currency :['',[Validators.required]]
    });
  }

  ngOnInit(): void {
  }

  public get currency() {
    return this.accountForm.get('currency') ;
  }

  public submitForm(data : any){
    
    console.log(data);
    
    if(!this.accountForm.valid){
      window.alert('Not valid!');
      return;
    }
    this.authenticate(data);
  }

  public authenticate(data : any){
 
    this.accountPostoji = this.accounts.filter((accF : AccountModel)=>accF.currency === data.currency)[0];

    if(this.accountPostoji){
      alert("Vec posjedujete racun u istoj valuti!");
    }
    else
    {
      this.accountService.createAccount(data).subscribe((acc : any)=>{
        this.accountNew = acc;
        console.log(this.accountNew);
        this.router.navigate(['/']);
        alert("Uspjesno kreiranje novog racuna!");
        this.accountForm.reset();
    });
    }
  }
}
