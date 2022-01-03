import { HttpClient, HttpResponse } from '@angular/common/http';
import { Component, OnInit, Output, ViewChild } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router, RouterLink } from '@angular/router';
import { EventEmitter } from '@angular/core'
import { UserModel } from '../models/user.model';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { HomeComponent } from '../home/home.component';
import { of, throwError } from 'rxjs';
import { ClientModel } from '../models/client.model';
import { ClientService } from '../services/client.service';


@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  public loginFrom : FormGroup;
  public userName : any;
  constructor(private formBuilder : FormBuilder,
    private ClientService : ClientService,private http:HttpClient,private router : Router) {

     // this.users = JSON.parse(localStorage.getItem('users')!);  /////////

      this.loginFrom = this.formBuilder.group({
        username:['',[Validators.required]],
        password:['',[Validators.required]]
      }); 
  }

  ngOnInit(): void {
  }

  public get username() {
    return this.loginFrom.get('username');
  }

  public get password() {
    return this.loginFrom.get('password') ;
  }

  public submitForm(data : any){
    
    console.log(data);
    
    if(!this.loginFrom.valid){
      window.alert('Not valid!');
      return;
    }
    
    this.ClientService.logIn(data).subscribe((client : any) =>{
      console.log(client.userType);
      if(client.userType == "admin"){
        this.router.navigate(['/admin']);
        localStorage.setItem('admin',JSON.stringify(client));
        alert("Admin uspjesno logovan!");
        this.loginFrom.reset();
      }
      else{
        this.router.navigate(['/']);
        localStorage.setItem('client',JSON.stringify(client));
        alert("Korisnik uspjesno logovan!");
        this.loginFrom.reset();
      }

    })
  }
}
