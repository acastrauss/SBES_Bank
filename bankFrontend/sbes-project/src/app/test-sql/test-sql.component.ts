import { HttpClient } from '@angular/common/http';
import { THIS_EXPR } from '@angular/compiler/src/output/output_ast';
import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { DomSanitizer } from '@angular/platform-browser';
import { UserService } from '../services/user.service';

@Component({
  selector: 'app-test-sql',
  templateUrl: './test-sql.component.html',
  styleUrls: ['./test-sql.component.css']
})
export class TestSqlComponent implements OnInit {
  private Url = "http://127.0.0.1:8000/api/sbesbank/";
  public testForm : FormGroup;
  public messageUpit : string;
  public trustedUrl: any;
  public dangerousUrl: any;

  
  constructor(private formBuilder : FormBuilder,private http : HttpClient,private Service : UserService, private sanitizer:DomSanitizer) {
    this.messageUpit = ";DELETE FROM SQLINJECTIONTEST";
    this.testForm = this.formBuilder.group({
      message : ['',[Validators.required]]
    });
    this.dangerousUrl = 'javascript:alert("XSS success")';
    this.trustedUrl = sanitizer.bypassSecurityTrustUrl(this.dangerousUrl);
  }

  ngOnInit(): void {
  }

  public submitForm(data : any){
    if(!this.testForm.valid){
      window.alert('Not valid!');
      return;
    }

    this.Service.test(data).subscribe((message : string)=>{
      window.alert(message);
    });

  }

}
