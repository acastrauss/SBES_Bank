import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { RegisterComponent } from './register/register.component';
import { HomeComponent } from './home/home.component';
import { NavigationComponent } from './navigation/navigation.component';
import { LoginComponent } from './login/login.component';
import { ReactiveFormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AccountSpliterComponent } from './spliters/account-spliter/account-spliter.component';
import { CardSpliterComponent } from './spliters/card-spliter/card-spliter.component';
import { AccountComponent } from './account/account.component';
import { CardComponent } from './card/card.component';
import { TransactionSpliterComponent } from './spliters/transaction-spliter/transaction-spliter.component';
import { TransactionInfoComponent } from './transaction-info/transaction-info.component';
import { TransactionFormComponent } from './transaction-form/transaction-form.component';
import { ExchangeFormComponent } from './exchange-form/exchange-form.component';
import { AdminComponent } from './admin/admin.component';

import { FormsModule } from '@angular/forms';
import { CreateAccountFormComponent } from './create-account-form/create-account-form.component';
import { CreatePaymentFormComponent } from './create-payment-form/create-payment-form.component';
@NgModule({
  declarations: [
    AppComponent,
    RegisterComponent,
    HomeComponent,
    NavigationComponent,
    LoginComponent,
    AccountSpliterComponent,
    CardSpliterComponent,
    AccountComponent,
    CardComponent,
    TransactionSpliterComponent,
    TransactionInfoComponent,
    TransactionFormComponent,
    ExchangeFormComponent,
    AdminComponent,
    CreateAccountFormComponent,
    CreatePaymentFormComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
