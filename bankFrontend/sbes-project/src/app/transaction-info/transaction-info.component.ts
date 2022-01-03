import { DOCUMENT } from '@angular/common';
import { Component, Inject, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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

    document.addEventListener("keydown", log);

    this.route.paramMap.subscribe(params =>{
      this.transactionsAcc = JSON.parse(localStorage.getItem('transactionsAcc')!);
      const transId : number = Number(params.get('id'));
      this.transaction = this.transactionsAcc.filter((trans : AccTransactionsModel) =>
          trans.id == transId)[0];
    });

    function log(event:any) {
      console.log(event.type); 
      console.log(event.keyCode);
      if(event.keyCode === 35){
        window.alert('Screenshot blokiran!');
      }
    }
  }

  ngOnInit(): void {
  }
}
