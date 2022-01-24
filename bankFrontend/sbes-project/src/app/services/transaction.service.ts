import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AccTransactionsModel } from '../models/accTransactions.model';
import { TransactionModel } from '../models/transaction.model';

@Injectable({
  providedIn: 'root'
})
export class TransactionService {
  private transactions : Observable<AccTransactionsModel[]>;
  private transactionUrl="http://127.0.0.1:8000/api/sbesbank/transactions";
  private createTransactionUrl="http://127.0.0.1:8000/api/sbesbank/doTransaction";
  private checkCurrencynUrl = "http://127.0.0.1:8000/api/sbesbank/checkCurrency";
  private createPaymentUrl = "http://127.0.0.1:8000/api/sbesbank/createpayment";
  private getPaymentUrl = "http://127.0.0.1:8000/api/sbesbank/createpayment";
  constructor(private http : HttpClient) {
    //this.transactions = new Observable<AccTransactionsModel[]>();
    //this.refreshTransactions();
  }

  private refreshTransactions(){
    this.transactions=this.http.get<AccTransactionsModel[]>(this.transactionUrl);
    return this.transactions;
  }

  public getTransactions(accountNumber : any):Observable<AccTransactionsModel[]>{
    const body ={
      accountNumber
    }
    console.log(body);
    return this.http.post<AccTransactionsModel[]>(this.transactionUrl,body);
  }

  public createTransaction(transactionObject : any) : Observable<any>{
    console.log(transactionObject)
    const body = { 
      ...transactionObject
    }
    console.log(body);
    return this.http.post<any>(this.createTransactionUrl,body);
  }

  public checkCurrency(accountNumber : any){
    const body = { 
      accountNumber
    }
    return this.http.post(this.checkCurrencynUrl,body);
  }

  public createPayment(data : any) : Observable<any>{
    const body = {
      data
    };
    return this.http.post<any>(this.createPaymentUrl,body);
  }


}
