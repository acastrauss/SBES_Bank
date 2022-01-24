import { DOCUMENT } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { timeout } from 'rxjs';
import { AccTransactionsModel } from '../models/accTransactions.model';

@Component({
  selector: 'app-transaction-info',
  templateUrl: './transaction-info.component.html',
  styleUrls: ['./transaction-info.component.css']
})
export class TransactionInfoComponent implements OnInit {

  public transactionsAcc : AccTransactionsModel[] ;
  public transaction : AccTransactionsModel;
  constructor(private route : ActivatedRoute,@Inject(DOCUMENT) private document: Document) {

   // const iDsakri= document.getElementById('iDsakri');

    document.addEventListener("keyup", log);
    document.addEventListener('copy', uncopyable);
    document.addEventListener('cut', uncopyable);

    this.route.paramMap.subscribe(params =>{
      this.transactionsAcc = JSON.parse(localStorage.getItem('transactionsAcc')!);
      const transId : number = Number(params.get('id'));
      this.transaction = this.transactionsAcc.filter((trans : AccTransactionsModel) =>
          trans.id == transId)[0];
    });

    function uncopyable(event:any){
      event.preventDefault();
      navigator.clipboard.writeText("Ne mozete kopirati ovaj tekst.");
    }

    function log(event:any) {
      console.log(event.keyCode)
      var toHide = document.getElementById("sakrij");
      if(event.keyCode == 44){
        
        var result = confirm( "Do you want to do this" );
        if(result){
          toHide.style.color= 'white';
          navigator.clipboard.writeText("nista");
          const myTimeout = setTimeout(myGreeting, 5000);
        }
      }
    }

    function myGreeting() {
      document.getElementById("sakrij").style.color = 'black';
    }

  }

  ngOnInit(): void {
  }
}
