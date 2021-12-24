import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TransactionListComponent } from './transaction-list/transaction-list.component';
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
@NgModule({
  declarations: [
    AppComponent,
    TransactionListComponent,
    RegisterComponent,
    HomeComponent,
    NavigationComponent,
    LoginComponent,
    AccountSpliterComponent,
    CardSpliterComponent,
    AccountComponent,
    CardComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    BrowserAnimationsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
