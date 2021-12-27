import { HttpClient, HttpClientModule, HttpParams } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { AccTransactionsModel } from '../models/accTransactions.model';
import { CardModel } from '../models/card.model';
import { UserModel } from '../models/user.model';
import { TransactionService } from '../services/transaction.service';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
  private accounts : AccountModel[] = [];
  private cardsAccUrl = "http://127.0.0.1:8000/api/sbesbank/accountCards";
  public cardsAccount : CardModel[];
  public account : AccountModel;
  public transactionsAcc : AccTransactionsModel[] ;

  constructor(private route : ActivatedRoute,private TransactionService : TransactionService,
    private http : HttpClient) {

  this.route.paramMap.subscribe(params =>{
    this.accounts= JSON.parse(localStorage.getItem('userAccounts')!);
    const accNum : string  = String(params.get('accountNumber'));
    this.account = this.accounts.filter((acc : AccountModel)=>acc.accountNumber === accNum)[0]; // cuvamo acc number iz URL-a
    /// da imamo u htmlu da acccount info opisemo 
    ;
    this.getCardsAcc();
    localStorage.setItem('account',JSON.stringify(this.account));
    this.TransactionService.getTransactions(accNum).subscribe((transactionsAcc : AccTransactionsModel[])=>{
          this.transactionsAcc=transactionsAcc;
          localStorage.setItem('transactionsAcc',JSON.stringify(this.transactionsAcc));
    });
  })
  }

  ngOnInit(): void {
  }

  public getCardsAcc():CardModel[]{
    if(this.account!=null){
      this.http.get<CardModel[]>(this.cardsAccUrl,{params:new HttpParams().set('accountId',this.account.id)} ).subscribe((cards : CardModel[])=>{
        this.cardsAccount=cards;
        console.log(this.cardsAccount);
        localStorage.setItem('cardsAccount',JSON.stringify(this.cardsAccount));
      });
  }
  
  console.log(this.account);
  return this.cardsAccount;
  }

}
