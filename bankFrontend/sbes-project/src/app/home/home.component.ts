import { HttpClient } from '@angular/common/http';
import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Observable, Subscription } from 'rxjs';
import { UserModel } from '../models/user.model';
import { UserService } from '../services/user.service';
@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit,OnDestroy {

  public define : boolean = false;
  private paramMapSub : Subscription ;
  public userName : any ;
  public loginUser : UserModel;

  private loginUserUrl = "htpp://localhost:3001/login/";

  constructor(private UserService : UserService,
              private route : ActivatedRoute,private http : HttpClient) { 
    this.loginUser = <UserModel>{};   
    this.define=true;
    this.paramMapSub = this.route.paramMap.subscribe(params =>{
    this.userName = params.get('username');
    
    // this.getUserById(this.userName).subscribe((user : UserModel)=>this.loginUser = user);
    /*
    this.UserService.getUsers().subscribe((users:UserModel[])=>{
                      users.forEach(u=>{if(u.username==this.userName){
                        this.loginUser=u;
                      }});
    });
    */      
  });
  }

  
  public getUserById(uName: string): Observable<UserModel> {
    return this.http.get<UserModel>(this.loginUserUrl + this.userName);
  }
  
  ngOnInit(): void {
  }

  ngOnDestroy(){
    if(this.paramMapSub !== null){
      this.paramMapSub.unsubscribe();
    }
  }

}
