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

  //public users : UserModel[] ;
  /*
  public loginUser: UserModel;
  public userId : number;
  
  private  loginUserId : any;
  private loginUserUrl = "htpp://localhost:3001/login/";
  */
 
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

  public submitForm(data : ClientModel){
    console.log(data);
    
    if(!this.loginFrom.valid){
      window.alert('Not valid!');
      return;
    }

    this.ClientService.logIn(data).subscribe((client : ClientModel) =>{
      // this.authenticate(data);
      this.router.navigate(['/']);
      localStorage.setItem('client',JSON.stringify(client));
      alert("Korisnik uspjesno logovan!");
      this.loginFrom.reset();
    })
  }

/*
  public authenticate(formData : any){

    const user = this.users.find(x=> x.username === formData.username  && x.password === formData.password);
    
    if (!user) 
      return error('Korisnicko ime ili lozinka nije korektna!');
    
      return ok({
        id:user.id,
        jmbg: user.jmbg,
        username: user.username,
        password: user.password,
        gender: user.gender,
        fullName : user.fullName,
        email: user.email,
        birthDate : user.birthDate,
        billingAddress : user.billingAddress
    })
  }
*/
}
/*
function ok(body? : UserModel) {
  return of(new HttpResponse({ status: 200, body }))
}
function error(message : string) {
  return throwError({ error: { message } });
}
*/
