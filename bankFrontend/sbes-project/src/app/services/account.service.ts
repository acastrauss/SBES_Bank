import { HttpClient, HttpParams } from '@angular/common/http';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AccountModel } from '../models/account.model';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private accounts: Observable<AccountModel[]>;
  private accountsUrl ="http://127.0.0.1:8000/api/sbesbank/getAccounts"; 
  private blockedUrl="http://127.0.0.1:8000/api/sbesbank/blockaccount";
  private createAccountUrl = "http://127.0.0.1:8000/api/sbesbank/createaccount ";
  constructor(private http: HttpClient) {
      this.accounts = new Observable<AccountModel[]>();  
      //this.refreshAccounts();
  }
  /*
  private refreshAccounts(){
    this.accounts=this.http.get<AccountModel[]>(this.accountsUrl);
    return this.accounts;
  }
  */
  public getAccounts(){
    this.accounts=this.http.get<AccountModel[]>(this.accountsUrl);
    return this.accounts;
  }
  public blocked(check : any,accNum : any):Observable<any>{
    const body = {
      check,accNum
    }
    console.log(body);
    return this.http.post<any>(this.blockedUrl,body);
  }

  public createAccount(fromData : any) : Observable<any>{
    const body = { 
      ...fromData
    }
    return this.http.post<any>(this.createAccountUrl,body);
  }

}
