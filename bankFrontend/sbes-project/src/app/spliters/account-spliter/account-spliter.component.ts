import { animate, style, transition, trigger } from '@angular/animations';
import { Component, Input, OnInit } from '@angular/core';
import { AccountModel } from 'src/app/models/account.model';
import { UserModel } from 'src/app/models/user.model';

@Component({
  selector: 'app-account-spliter',
  templateUrl: './account-spliter.component.html',
  styleUrls: ['./account-spliter.component.css'],
  animations: [
    trigger('carouselAnimation', [
      transition('void => *', [
        style({ opacity: 0 }),
        animate('300ms', style({ opacity: 1 }))
      ]),
      transition('* => void', [
        animate('300ms', style({ opacity: 0 }))
      ])
    ])
  ]
})
export class AccountSpliterComponent implements OnInit {

  public client : UserModel = JSON.parse(localStorage.getItem('client')!);
  
  @Input() userAccounts : AccountModel[]; 

  constructor() {}

  ngOnInit(): void {
  }

  //@Input() accounts;


  currentSlide = 0;
  onPreviousClick() {
    const previous = this.currentSlide - 1;
    this.currentSlide = previous < 0 ? this.userAccounts.length - 1 : previous;
    console.log("previous clicked, new current slide is: ", this.currentSlide);
  }

  onNextClick() {
    const next = this.currentSlide + 1;
    this.currentSlide = next === this.userAccounts.length ? 0 : next;
    console.log("next clicked, new current slide is: ", this.currentSlide);
  }

}
