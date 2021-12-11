import { TestBed } from '@angular/core/testing';

import { SbesbankService } from './sbesbank.service';

describe('SbesbankService', () => {
  let service: SbesbankService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SbesbankService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
