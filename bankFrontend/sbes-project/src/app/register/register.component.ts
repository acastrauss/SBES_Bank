import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { ClientModel } from '../models/client.model';
import { ClientService } from '../services/client.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  public users : ClientModel[] ;
  public registerForm : FormGroup;

  constructor(private formBuilder : FormBuilder,private router : Router,
              private ClientService : ClientService) {

    this.users = JSON.parse(localStorage.getItem('users')!);  /////////

    this.registerForm = this.formBuilder.group({
      username:['',[Validators.required]],
      password:['',[Validators.required]],
      billingAddress:['',[Validators.required]],
      birthDate:['',[Validators.required]],
      email:['',[Validators.required,Validators.email]],
      fullName:['',[Validators.required]],
      gender:['',[Validators.required]],
      jmbg:['',[Validators.required]]
    })

  }
  ngOnInit(): void {
  }

  public get username() {
    return this.registerForm.get('username');
  }

  public get password() {
    return this.registerForm.get('password') ;
  }

  public get billingAddress() {
    return this.registerForm.get('billingAddress');
  }

  public get birthDate() {
    return this.registerForm.get('birthDate') ;
  }

  public get email() {
    return this.registerForm.get('email');
  }

  public get fullName() {
    return this.registerForm.get('fullName') ;
  }

  public get gender() {
    return this.registerForm.get('gender');
  }

  public get jmbg() {
    return this.registerForm.get('jmbg') ;
  }


  public submitForm(data : any){
    console.log(data);
    
    if(!this.registerForm.valid){
      window.alert('Not valid!');
      return;
    }

    this.ClientService.register(data).subscribe((user : ClientModel) =>{
     // this.authenticate(user);
      window.alert('Korisnik uspjesno registrovan!');
      this.router.navigate(['/login']);
     // this.users.push(data);///mozda cu morati data kastovati 
     // localStorage.setItem('users', JSON.stringify(this.users));      
      this.registerForm.reset();
    })
  }

  public authenticate(formData : any){

    const user = this.users.find(x=> x.userId.username === formData.username  && x.userId.password === formData.password 
      && x.userId.fullName === formData.fullName);
    
    if(user) 
      return ok({
        id : user.id,
        userId:{
          id : user.userId.id,
          jmbg: user.userId.jmbg,
          username: user.userId.username,
          password: user.userId.password,
          gender: user.userId.gender,
          fullName : user.userId.fullName,
          email: user.userId.email,
          birthDate : user.userId.birthDate,
          billingAddress : user.userId.billingAddress,
          userType:"client"
        }
    })
    return error('Korisnik ${user.fullName} vec postoji,pokusajte ponovo!');
  }
  }

  function ok(body? : ClientModel)  {
    return of(new HttpResponse({ status: 200, body }))
  }
  
  function error(message : string) {
    return throwError({ error: { message } });
  }


