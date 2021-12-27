import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { AccountModel } from '../models/account.model';
import { CardModel } from '../models/card.model';
import { ClientModel } from '../models/client.model';
import { UserModel } from '../models/user.model';
import { CardService } from '../services/card.service';

@Component({
  selector: 'app-card',
  templateUrl: './card.component.html',
  styleUrls: ['./card.component.css']
})
export class CardComponent implements OnInit {
  public cardHolder : ClientModel;
  public accNum : AccountModel ;
  public cardForm : FormGroup;
  public cards : CardModel[];
  public cardPostoji : CardModel;
  constructor(private formBuilder : FormBuilder,private cardService : CardService,private router : Router) { 
    
    this.accNum= JSON.parse(localStorage.getItem('account')!);
    this.cardHolder = JSON.parse(localStorage.getItem('client')!);
    this.cards= JSON.parse(localStorage.getItem('cardsAccount')!);

    this.cardForm = this.formBuilder.group({
      accNum :[''],
      cardHolder :[''],
      cardType:['',[Validators.required]],
      cardProcessor:['',[Validators.required]]
    });
    
  }

  ngOnInit(): void {
  }

  public get cardType() {
    return this.cardForm.get('cardType');
  }

  public get cardProcessor() {
    return this.cardForm.get('cardProcessor') ;
  }

  public submitForm(data : CardModel){
    console.log(data);
    
    if(!this.cardForm.valid){
      window.alert('Not valid!');
      return;
    }
    this.authenticate(data);
  }


  public authenticate(data : any){
 
    this.cardPostoji = this.cards.filter((accF : CardModel)=>accF.cardType === data.cardType && accF.cardProcessor === data.cardProcessor)[0];

    if(this.cardPostoji){
      alert("Vec posjedujete takvu karticu!");
    }
    else
    {
      this.cardService.createCard(data).subscribe((card : CardModel) =>{
        this.router.navigate(['/']);
        //localStorage.setItem('card',JSON.stringify(card));
        alert("Kartica uspjesno kreirana!");
        this.cardForm.reset();
      });
    }
  }



}
