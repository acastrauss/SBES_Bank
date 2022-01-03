import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { UserModel } from '../models/user.model';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  private registerUrl = "http://127.0.0.1:8000/api/sbesbank/registeruser";

  constructor(private http : HttpClient) { }

  public register(data : UserModel) : Observable<UserModel>{
    const body ={
      ...data
    }
    return this.http.post<UserModel>(this.registerUrl,body);
  }

}
