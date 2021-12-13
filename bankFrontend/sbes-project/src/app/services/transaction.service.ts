import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { TransactionModel } from '../models/transaction.model';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  private transactions : Observable<TransactionModel[]>;
  private transactionUrl="http://localhost:3001/transactions/";
  
  constructor(private http : HttpClient) {
    this.transactions = new Observable<TransactionModel[]>();
    this.refreshTransactions();
  }

  private refreshTransactions(){
    this.transactions=this.http.get<TransactionModel[]>(this.transactionUrl);
    return this.transactions;
  }

  public getTransactions(){
    return this.transactions;
  }
}
