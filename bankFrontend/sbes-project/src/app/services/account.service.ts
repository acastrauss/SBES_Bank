import { HttpClient } from '@angular/common/http';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { AccountModel } from '../models/account.model';

@Injectable({
  providedIn: 'root'
})
export class AccountService {
  private accounts: Observable<AccountModel[]>;
  private readonly accountsUrl ="http://localhost:3001/accounts/"; 
  
  constructor(private http: HttpClient) {
      this.accounts = new Observable<AccountModel[]>();  
      this.refreshAccounts();
  }

  private refreshAccounts(){
    this.accounts=this.http.get<AccountModel[]>(this.accountsUrl);
    return this.accounts;
  }

  public getAccounts(){
    return this.accounts;
  }

}
