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
import * as Forge from 'node-forge';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  public loginFrom : FormGroup;
  public userName : any;
  private publicKey : string;
  private dataString : string;

  constructor(private formBuilder : FormBuilder,
    private ClientService : ClientService,private http:HttpClient,private router : Router) {

     // this.users = JSON.parse(localStorage.getItem('users')!);  /////////

     this.publicKey = JSON.parse(localStorage.getItem('sertificate')!); 

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
  
    if(!this.loginFrom.valid){
      window.alert('Not valid!');
      return;
    }
    
    this.dataString = JSON.stringify(data);
    console.log(this.dataString.length)
    data = this.encryptWithPublicKey(this.dataString);
    console.log(data.length)
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


  public encryptWithPublicKey(valueToEncrypt: string): string {
    const rsa = Forge.pki.publicKeyFromPem(this.publicKey);
    
    return rsa.encrypt(valueToEncrypt);
  }


}
