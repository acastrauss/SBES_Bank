import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ClientModel } from '../models/client.model';

@Injectable({
  providedIn: 'root'
})
export class ClientService {

  private clients: Observable<ClientModel[]>;
  private usersUrl = "http://127.0.0.1:8000/api/sbesbank/loginuser";

  private registerUrl = "http://127.0.0.1:8000/api/sbesbank/registeruser";

  constructor(private http : HttpClient) { 
    this.clients = new Observable<ClientModel[]>();
    this.refreshUsers();
  }

  public getUsers(){
    return this.clients;
  }
  private refreshUsers(){
    this.clients=this.http.get<ClientModel[]>(this.usersUrl);
    return this.clients;
  }
  public logIn(formData : any) : Observable<any>{
    const body = {
      ...formData
    };
    return this.http.post<any>(this.usersUrl,body);
  }

  public register(data : ClientModel) : Observable<ClientModel>{
    const body ={
      ...data
    }
    return this.http.post<ClientModel>(this.registerUrl,body);
  }

}
