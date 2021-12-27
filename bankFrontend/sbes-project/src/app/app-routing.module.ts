import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AccountComponent } from './account/account.component';
import { AdminComponent } from './admin/admin.component';
import { CardComponent } from './card/card.component';
import { CreateAccountFormComponent } from './create-account-form/create-account-form.component';
import { CreatePaymentFormComponent } from './create-payment-form/create-payment-form.component';
import { ExchangeFormComponent } from './exchange-form/exchange-form.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { RegisterComponent } from './register/register.component';
import { TransactionFormComponent } from './transaction-form/transaction-form.component';
import { TransactionInfoComponent } from './transaction-info/transaction-info.component';

const routes: Routes = [
  {path:'',component: HomeComponent},
  {path: 'register',component:RegisterComponent},
  {path: 'login',component:LoginComponent },
  {path: 'account/:accountNumber',component:AccountComponent}, 
  {path: 'card',component:CardComponent },
  {path: 'transaction-info/:id',component:TransactionInfoComponent},
  {path: 'transaction-form',component:TransactionFormComponent},
  {path: 'exchange-form',component:ExchangeFormComponent},
  {path : 'admin',component: AdminComponent},
  {path : 'create-payment-form',component:CreatePaymentFormComponent},
  {path : 'create-account-form',component:CreateAccountFormComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
