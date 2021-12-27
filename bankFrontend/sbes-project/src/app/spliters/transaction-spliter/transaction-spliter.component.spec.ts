import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TransactionSpliterComponent } from './transaction-spliter.component';

describe('TransactionSpliterComponent', () => {
  let component: TransactionSpliterComponent;
  let fixture: ComponentFixture<TransactionSpliterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TransactionSpliterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TransactionSpliterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
