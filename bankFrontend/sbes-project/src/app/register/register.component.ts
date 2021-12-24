import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { of, throwError } from 'rxjs';
import { ClientModel } from '../models/client.model';
import { ClientService } from '../services/client.service';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  public users : ClientModel[] ;
  public registerFrom : FormGroup;

  constructor(private formBuilder : FormBuilder,
              private ClientService : ClientService) {

    this.users = JSON.parse(localStorage.getItem('users')!);  /////////

    this.registerFrom = this.formBuilder.group({
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
    return this.registerFrom.get('username');
  }

  public get password() {
    return this.registerFrom.get('password') ;
  }

  public get billingAddress() {
    return this.registerFrom.get('billingAddress');
  }

  public get birthDate() {
    return this.registerFrom.get('birthDate') ;
  }

  public get email() {
    return this.registerFrom.get('email');
  }

  public get fullName() {
    return this.registerFrom.get('fullName') ;
  }

  public get gender() {
    return this.registerFrom.get('gender');
  }

  public get jmbg() {
    return this.registerFrom.get('jmbg') ;
  }


  public submitForm(data : ClientModel){
    console.log(data);
    
    if(!this.registerFrom.valid){
      window.alert('Not valid!');
      return;
    }

    this.ClientService.register(data).subscribe((user : ClientModel) =>{
      this.authenticate(data);
      window.alert('Korisnik ${user.username} uspjesno registrovan!');
      this.users.push(data);///mozda cu morati data kastovati 
      localStorage.setItem('users', JSON.stringify(this.users));      
      this.registerFrom.reset();
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
          billingAddress : user.userId.billingAddress
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


