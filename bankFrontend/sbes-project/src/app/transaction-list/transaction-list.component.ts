import { Component, OnInit } from '@angular/core';
import { TransactionModel } from '../models/transaction.model';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-transaction-list',
  templateUrl: './transaction-list.component.html',
  styleUrls: ['./transaction-list.component.css']
})
export class TransactionListComponent implements OnInit {

  public transactions : TransactionModel[] =[];

  constructor(private transService : TransactionService) { 
    this.transService.getTransactions()
    .subscribe((transactions: TransactionModel[])  => {
      this.transactions = transactions;
    });
  }

  ngOnInit(): void {
  }

}
