import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Iuser } from '../models/iuser.model';


const baseUrl = 'http://localhost:8080/api/iusers';
@Injectable({
  providedIn: 'root'
})




export class SbesbankService {

  constructor(private http: HttpClient) { }
  
  getAll(): Observable<Iuser[]> {
    return this.http.get<Iuser[]>(baseUrl);
  }

  get(id: any): Observable<Iuser> {
    return this.http.get(`${baseUrl}/${id}`);
  }

  create(data: any): Observable<any> {
    return this.http.post(baseUrl, data);
  }

}
