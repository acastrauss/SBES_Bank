import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TestSqlComponent } from './test-sql.component';

describe('TestSqlComponent', () => {
  let component: TestSqlComponent;
  let fixture: ComponentFixture<TestSqlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TestSqlComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TestSqlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
