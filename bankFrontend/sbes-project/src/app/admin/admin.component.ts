import { Component, OnInit } from '@angular/core';
import { AccountModel } from '../models/account.model';
import { UserModel } from '../models/user.model';
import { AccountService } from '../services/account.service';
@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.css']
})
export class AdminComponent implements OnInit {

  public accounts : AccountModel[] = [];
  public admin : UserModel;
  public isChecked : any;
  constructor(private AccountService : AccountService) {
    this.admin = JSON.parse(localStorage.getItem('admin')!); 
    this.AccountService.getAccounts().subscribe((accs : AccountModel[])=>{
        this.accounts = accs;
    })

  }

  ngOnInit(): void {
  }

  public checkValue(event: any,accNum : string){
    console.log(accNum)
    console.log(event.currentTarget.checked);
    this.AccountService.blocked(event.currentTarget.checked,accNum).subscribe((jsonss:any)=>{
      this.isChecked=jsonss;
      console.log(this.isChecked);
    });
 }

}
