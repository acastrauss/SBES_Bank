import { Component, Input, OnInit } from '@angular/core';
import { AccTransactionsModel } from 'src/app/models/accTransactions.model';

@Component({
  selector: 'app-transaction-spliter',
  templateUrl: './transaction-spliter.component.html',
  styleUrls: ['./transaction-spliter.component.css']
})
export class TransactionSpliterComponent implements OnInit {
 
  @Input() transactionsAcc : AccTransactionsModel[]; 
 
  constructor() { }

  ngOnInit(): void {
  }

  currentSlide = 0;
  onPreviousClick() {
    const previous = this.currentSlide - 1;
    this.currentSlide = previous < 0 ? this.transactionsAcc.length - 1 : previous;
    console.log("previous clicked, new current slide is: ", this.currentSlide);
  }

  onNextClick() {
    const next = this.currentSlide + 1;
    this.currentSlide = next === this.transactionsAcc.length ? 0 : next;
    console.log("next clicked, new current slide is: ", this.currentSlide);
  }

}
