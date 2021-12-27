import { Component, OnInit } from '@angular/core';
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

  constructor(private route : ActivatedRoute) {
    this.route.paramMap.subscribe(params =>{
      this.transactionsAcc = JSON.parse(localStorage.getItem('transactionsAcc')!);
      const transId : number = Number(params.get('id'));
      this.transaction = this.transactionsAcc.filter((trans : AccTransactionsModel) =>
          trans.id == transId)[0];
    })
  }

  ngOnInit(): void {
  }

}
