import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserModel } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private users: Observable<UserModel[]>;
  private usersUrl = "http://127.0.0.1:8000/api/sbesbank/loginuser";
  private registerUrl = "http://127.0.0.1:8000/api/sbesbank/registeruser"

  constructor(private htpp : HttpClient) { 
    this.users = new Observable<UserModel[]>();
    this.refreshUsers();
  }

  public getUsers(){
    return this.users;
  }
  private refreshUsers(){
    this.users=this.htpp.get<UserModel[]>(this.usersUrl);
    return this.users;
  }
  public logIn(formData : any) : Observable<UserModel>{
    const body = {
      ...formData
    };
    return this.htpp.post<UserModel>(this.usersUrl,body);
  }

  public register(formData : any) : Observable<UserModel>{
    const body ={
      ...formData
    }
    return this.htpp.post<UserModel>(this.registerUrl,body);
  }
}
