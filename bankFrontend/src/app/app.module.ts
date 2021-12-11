import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import {APP_BASE_HREF} from '@angular/common';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AddUserComponent } from './components/add-user/add-user.component';


@NgModule({
  declarations: [
    AppComponent,
    AddUserComponent,
  ],
  imports: [
    HttpClientModule,
    BrowserModule,
    AppRoutingModule,
    FormsModule
  ],
  providers: [{provide: APP_BASE_HREF, useValue: '/my/app'}],
  bootstrap: [AppComponent]
})
export class AppModule { }

