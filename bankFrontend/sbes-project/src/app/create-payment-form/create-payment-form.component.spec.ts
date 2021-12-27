import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CreatePaymentFormComponent } from './create-payment-form.component';

describe('CreatePaymentFormComponent', () => {
  let component: CreatePaymentFormComponent;
  let fixture: ComponentFixture<CreatePaymentFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ CreatePaymentFormComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(CreatePaymentFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
