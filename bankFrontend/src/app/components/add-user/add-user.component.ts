import { Component, OnInit } from '@angular/core';

import { Iuser } from 'src/app/models/iuser.model';
import { SbesbankService } from 'src/app/services/sbesbank.service';
@Component({
  selector: 'app-add-user',
  templateUrl: './add-user.component.html',
  styleUrls: ['./add-user.component.css']
})
export class AddUserComponent implements OnInit {

  iuser: Iuser = {
    fullName: '',
    billingAddress: ''
  };
  submitted = false;

  constructor(private sbesbankService: SbesbankService) { }

  ngOnInit(): void {
  }

  saveIUser(): void {
    const data = {
      fullName: this.iuser.fullName,
      billingAddress: this.iuser.billingAddress
    };

    this.sbesbankService.create(data)
      .subscribe(
        response => {
          console.log(response);
          this.submitted = true;
        },
        error => {
          console.log(error);
        });
  }

  newIUser(): void {
    this.submitted = false;
    this.iuser = {
      fullName: '',
      billingAddress: ''
    };
  }
}