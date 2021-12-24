import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AccountSpliterComponent } from './account-spliter.component';

describe('AccountSpliterComponent', () => {
  let component: AccountSpliterComponent;
  let fixture: ComponentFixture<AccountSpliterComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ AccountSpliterComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(AccountSpliterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
