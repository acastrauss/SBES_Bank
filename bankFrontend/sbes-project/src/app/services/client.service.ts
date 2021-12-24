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


  constructor(private htpp : HttpClient) { 
    this.clients = new Observable<ClientModel[]>();
    this.refreshUsers();
  }

  public getUsers(){
    return this.clients;
  }
  private refreshUsers(){
    this.clients=this.htpp.get<ClientModel[]>(this.usersUrl);
    return this.clients;
  }
  public logIn(formData : any) : Observable<ClientModel>{
    const body = {
      ...formData
    };
    return this.htpp.post<ClientModel>(this.usersUrl,body);
  }

  public register(formData : any) : Observable<ClientModel>{
    const body ={
      ...formData
    }
    return this.htpp.post<ClientModel>(this.usersUrl,body);
  }

}
