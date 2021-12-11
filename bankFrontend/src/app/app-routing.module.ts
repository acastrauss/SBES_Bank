import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AddUserComponent } from './components/add-user/add-user.component';
const routes: Routes = [
  { path: '', redirectTo: 'iusers', pathMatch: 'full' },
  { path: 'add', component: AddUserComponent }

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
