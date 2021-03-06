import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { CardModel } from '../models/card.model';

@Injectable({
  providedIn: 'root'
})
export class CardService {
  private cards : Observable<CardModel[]>;
  private cardsUrl = "http://127.0.0.1:8000/api/sbesbank/createNewCard";
  
  constructor(private http: HttpClient) {
    this.cards = new Observable<CardModel[]>(); 
    this.refreshCards();
  }

  private refreshCards() : Observable<CardModel[]>{
    this.cards=this.http.get<CardModel[]>(this.cardsUrl);
    return this.cards;
  }

  public getCards() : Observable<CardModel[]>{
    return this.cards;
  }

  public createCard(formData : any) : Observable<CardModel>{
    const body = {
      ...formData
    };
    return this.http.post<CardModel>(this.cardsUrl,body);
  }
}
