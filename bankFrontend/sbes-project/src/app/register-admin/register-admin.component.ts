import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { UserModel } from '../models/user.model';
import { AdminService } from '../services/admin.service';
import { ClientService } from '../services/client.service';

@Component({
  selector: 'app-register-admin',
  templateUrl: './register-admin.component.html',
  styleUrls: ['./register-admin.component.css']
})
export class RegisterAdminComponent implements OnInit {

  public registerForm : FormGroup;
  
  constructor(private formBuilder : FormBuilder,private router : Router,private AdminService : AdminService) { 

    this.registerForm = this.formBuilder.group({
      username:['',[Validators.required]],
      password:['',[Validators.required]],
      billingAddress:['',[Validators.required]],
      birthDate:['',[Validators.required]],
      email:['',[Validators.required,Validators.email]],
      fullName:['',[Validators.required]],
      gender:['',[Validators.required]],
      jmbg:['',[Validators.required,Validators.pattern]]
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

  public submitForm(data : UserModel){
    console.log(data);
    data.userType = "admin";

    if(!this.registerForm.valid){
      window.alert('Not valid!');
      return;
    }

    this.AdminService.register(data).subscribe((user : UserModel) =>{
      window.alert('Admin uspjesno registrovan!');
      this.router.navigate(['/admin']);   
      this.registerForm.reset();
    })
  }

}
