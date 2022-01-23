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
import * as CryptoJS from 'crypto-js';
import {JSEncrypt} from 'jsencrypt';
import * as rs from 'jsrsasign';

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
  private dataMess : string;
  private fileName : string;
  private privateKey : any;

  constructor(private formBuilder : FormBuilder,
    private ClientService : ClientService,private http:HttpClient,private router : Router) {

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

  public async submitForm(data : any){
  
    if(!this.loginFrom.valid){
      window.alert('Not valid!');
      return;
    }
    data['password']= CryptoJS.SHA256(data['password']).toString();

    data.message = "bilo sta";
    data.signature = CryptoJS.SHA256(data.message).toString();
    this.dataMess = data.signature;
             //signature kriptovano,mess obicna por
    data.signature = this.encryptWithPrivateKey(this.dataMess).toString();
    

    // let pkey = rs.KEYUTIL.getKey(this.privateKey);
    // var sign = new rs.KJUR.crypto.Signature({
    //   "alg":"SHA1withRSA"
    // });
    // sign.init(pkey);
    // var signVal = sign.signString(data.signature);
    // data.signature = signVal;

    localStorage.setItem('signature', data.signature);
    
    for(var i in data){
      if(i != 'signature'){
        data[i]= this.encryptWithPublicKey(data[i]);
      }
    }

    console.log(data);
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

    let encrypt = new JSEncrypt();
    encrypt.setPublicKey(this.publicKey);
    return encrypt.encrypt(valueToEncrypt);
  }

  public encryptWithPrivateKey(valueToEncrypt: string): string {

    let encrypt = new JSEncrypt();
    encrypt.setPrivateKey(this.privateKey);
    return encrypt.encrypt(valueToEncrypt);
  }

  public onFileSelected(event : any) {

    const file:File = event.target.files[0];

    let fileReader : FileReader = new FileReader();

    if (file) {

        this.fileName = file.name;
        fileReader.onload = (event)=>{
          this.privateKey = fileReader.result;
          localStorage.setItem('privateSert',JSON.stringify(this.privateKey));
        }
        fileReader.readAsText(file);
     
    }
}
}
