import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardSpliterComponent } from './card-spliter.component';

describe('CardSpliterComponent', () => {
  let component: CardSpliterComponent;
  let fixture: ComponentFixture<CardSpliterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CardSpliterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CardSpliterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
