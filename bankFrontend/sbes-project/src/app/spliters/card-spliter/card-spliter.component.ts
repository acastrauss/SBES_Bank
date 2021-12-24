import { animate, style, transition, trigger } from '@angular/animations';
import { Component, Input, OnInit } from '@angular/core';
import { CardModel } from 'src/app/models/card.model';

@Component({
  selector: 'app-card-spliter',
  templateUrl: './card-spliter.component.html',
  styleUrls: ['./card-spliter.component.css'],
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
export class CardSpliterComponent implements OnInit {

  constructor() { }

  ngOnInit(): void {
  }

  @Input() cardsAccount : CardModel[]; 
  //@Input() accounts;

  currentSlide = 0;

  onPreviousClick() {
    const previous = this.currentSlide - 1;
    this.currentSlide = previous < 0 ? this.cardsAccount.length - 1 : previous;
    console.log("previous clicked, new current slide is: ", this.currentSlide);
  }

  onNextClick() {
    const next = this.currentSlide + 1;
    this.currentSlide = next === this.cardsAccount.length ? 0 : next;
    console.log("next clicked, new current slide is: ", this.currentSlide);
  }


}
