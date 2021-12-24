import { HttpClient, HttpClientModule } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { UserModel } from '../models/user.model';

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.css']
})
export class AccountComponent implements OnInit {
  private accounts : AccountModel[] = [];
  public account : AccountModel;
  constructor(private route : ActivatedRoute) {

  this.route.paramMap.subscribe(params =>{
    this.accounts= JSON.parse(localStorage.getItem('userAccounts')!);
    const accNum : string  = String(params.get('accountNumber'));
    this.account = this.accounts.filter((acc : AccountModel)=>acc.accountNumber === accNum)[0]; // cuvamo acc number iz URL-a
    /// da imamo u htmlu da acccount info opisemo 
    localStorage.setItem('account',JSON.stringify(this.account));
  })

  }

  ngOnInit(): void {
  }

}
