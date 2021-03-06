import { HttpResponse } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import { of, throwError } from 'rxjs';
import { ClientModel } from '../models/client.model';
import { ClientService } from '../services/client.service';
import * as CryptoJS from 'crypto-js';
import {JSEncrypt} from 'jsencrypt';
import { CardModel } from '../models/card.model';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css']
})
export class RegisterComponent implements OnInit {
  
  public users : ClientModel[] ;
  public registerForm : FormGroup;
  private publicKey : string;
  private dataString : string;

  constructor(private formBuilder : FormBuilder,private router : Router,
              private ClientService : ClientService) {

    this.users = JSON.parse(localStorage.getItem('users')!);  /////////
    
    this.publicKey = JSON.parse(localStorage.getItem('sertificate')!); 
              

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


  public submitForm(data : any){
    data.userType = "client";

    if(!this.registerForm.valid){
      window.alert('Not valid!');
      return;
    }
    data['password']= CryptoJS.SHA256(data['password']).toString();
   
    for(var i in data){
      data[i]= this.encryptWithPublicKey(data[i]);
    }

    console.log(data);
    this.ClientService.register(data).subscribe((card : CardModel) =>{
     // this.authenticate(user);
      console.log(card)
      localStorage.setItem('cvc',JSON.stringify(card.cvc));
      localStorage.setItem('pin',JSON.stringify(card.pin));

      localStorage.setItem('sertificatePrivate',JSON.stringify(card.key));

      this.download(card.key);


      window.alert('Korisnik uspjesno registrovan,cvc kreirane kartice:'+' ' + card.cvc +' , ' + 'pin kreirane kartice:'+ ' ' + card.pin);
      this.router.navigate(['/login']);
     // this.users.push(data);///mozda cu morati data kastovati 
     // localStorage.setItem('users', JSON.stringify(this.users));      
      this.registerForm.reset();
    })
  }

  public download(key : string) {
    let file = new Blob([key], {type: '.key'});
    let a = document.createElement("a"),
            url = URL.createObjectURL(file);
    a.href = url;
    a.download = "my_certificate.key";
    document.body.appendChild(a);
    a.click();
    setTimeout(function() {
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);  
    }, 0); 
}

  public encryptWithPublicKey(valueToEncrypt: any): string {

    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(this.publicKey);
    return encrypt.encrypt(String(valueToEncrypt));
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

