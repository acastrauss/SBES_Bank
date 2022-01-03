import { HttpClient, HttpParams } from '@angular/common/http';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { AccountModel } from '../models/account.model';
import { CardModel } from '../models/card.model';
import { ClientModel } from '../models/client.model';
import { UserModel } from '../models/user.model';
import { UserService } from '../services/user.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit{
  //public userAccounts : Observable<AccountModel[]>;
  public path : string = "http://127.0.0.1:8000/api/sbesbank/";
  public userAccounts:AccountModel[];
  public cardsAccount:CardModel[];
  public logInClient : ClientModel ;
  public logInAdmin : UserModel;
  private userAccountsUrl = "http://127.0.0.1:8000/api/sbesbank/accountinfo/";
  constructor(private UserService : UserService,
              private route : ActivatedRoute,private http : HttpClient) { 

    localStorage.setItem('path',JSON.stringify(this.path));

    this.logInClient = JSON.parse(localStorage.getItem('client')!);
    this.logInAdmin = JSON.parse(localStorage.getItem('admin')!);
    this.getAccUser();   
    //this.getCardsUser();     
    }
    /*
    this.paramMapSub = this.route.paramMap.subscribe(params =>{
    this.userName = params.get('username');
    
    // this.getUserById(this.userName).subscribe((user : UserModel)=>this.loginUser = user);
    /*
    this.UserService.getUsers().subscribe((users:UserModel[])=>{
                      users.forEach(u=>{if(u.username==this.userName){
                        this.loginUser=u;
                      }});
    });    
  });
    */  
  
  /*
  public getUserById(uName: string): Observable<UserModel> {
    return this.http.get<UserModel>(this.loginUserUrl + this.userName);
  }
  */
  ngOnInit(): void {
  }

  public getAccUser():AccountModel[]{
    if(this.logInClient!=null){
      this.http.get<AccountModel[]>(this.userAccountsUrl,{params:new HttpParams().set('id',this.logInClient.id)} ).subscribe((acc : AccountModel[])=>{
        this.userAccounts=acc;
        localStorage.setItem('userAccounts',JSON.stringify(this.userAccounts));
      });
  }
  return this.userAccounts;
}
}
