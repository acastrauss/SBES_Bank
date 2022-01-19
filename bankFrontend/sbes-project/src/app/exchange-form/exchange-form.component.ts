import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { ExchangeModel } from '../models/exchange.model';
import { ExchangeService } from '../services/exchange.service';

import * as CryptoJS from 'crypto-js';
import {JSEncrypt} from 'jsencrypt';
@Component({
  selector: 'app-exchange-form',
  templateUrl: './exchange-form.component.html',
  styleUrls: ['./exchange-form.component.css']
})
export class ExchangeFormComponent implements OnInit {

  private account : AccountModel;
  public accounts : AccountModel[];
  public exchangeForm : FormGroup;
  public json:any;
  private publicKey : string;
  private dataString : string;
  constructor(private formBuilder : FormBuilder,private exchangeService : ExchangeService,
              private router : Router) { 
    this.accounts= JSON.parse(localStorage.getItem('userAccounts')!)

    this.publicKey = JSON.parse(localStorage.getItem('sertificate')!); 
    

    this.exchangeForm = this.formBuilder.group({
        accountFrom: ['',[Validators.required]],
        accountTo: ['',[Validators.required]],
        amount: ['',[Validators.required]],
    })
  }

  ngOnInit(): void {
  }

  public get accountFrom() {
    return this.exchangeForm.get('accountFrom');
  }

  public get accountTo() {
    return this.exchangeForm.get('accountTo') ;
  }
  public get amount() {
    return this.exchangeForm.get('amount');
  }

  public submitForm(data : ExchangeModel){
    
    if(!this.exchangeForm.valid){
      window.alert('Not valid!');
      return;
    }

    this.authenticate(data);
  }

  
  public encryptWithPublicKey(valueToEncrypt: any): string {

    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(this.publicKey);
    return encrypt.encrypt(String(valueToEncrypt));
  }
  public authenticate(data : ExchangeModel){

    this.account = this.accounts.filter((acc : AccountModel)=>acc.accountNumber === data.accountFrom)[0];

    if(data.accountFrom === data.accountTo){
      return window.alert('Nemoguce izvrsiti promijenu novca sa istog racuna!');
    }
    else if(this.account.accountBalance < data.amount){
      return window.alert('Nemate dovoljno sredstava na racunu!');
    }
    else
    {
      
      this.json = JSON.parse(JSON.stringify(data));

      for(var i in this.json){
        this.json[i]= this.encryptWithPublicKey(this.json[i]);
      }
      console.log(this.json);
      this.exchangeService.createExchange(this.json).subscribe((ex : ExchangeModel) =>{
        this.router.navigate(['/account',data.accountFrom]);
        this.exchangeForm.reset();
        return window.alert('Mijenjanje novca uspjesno obavljeno!');
      })
    }
  }

}
