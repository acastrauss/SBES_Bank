import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ExchangeModel } from '../models/exchange.model';

@Injectable({
  providedIn: 'root'
})
export class ExchangeService {

  private createExchangeUrl = "http://127.0.0.1:8000/api/sbesbank/exchangeMoney";

  constructor(private http : HttpClient) { }


  public createExchange(amountEx : ExchangeModel) : Observable<ExchangeModel>{
    const body = { 
      ...amountEx
    }
    return this.http.post<ExchangeModel>(this.createExchangeUrl,body);
  }
}
