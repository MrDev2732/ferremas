import { NgModule } from '@angular/core';
import { Route, RouterModule } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { TiendaComponent } from './components/tienda/tienda.component';
import { LoginComponent } from './components/login/login.component';
import { AdminComponent } from './components/admin/admin.component';
import { CarritoComponent } from './components/carrito/carrito.component';
import { VendedorComponent } from './components/vendedor/vendedor.component';
import { BodegueroComponent } from './components/bodeguero/bodeguero.component';
import { AuthGuard } from './guards/auth.guard';

export const appRoutes: Route[] = [
  { path: '', component: HomeComponent },
  { path: 'tienda', component: TiendaComponent },
  { path: 'login', component: LoginComponent },
  { path: 'admin', component: AdminComponent, canActivate: [AuthGuard], data: { expectedRoles: ['ADMINISTRADOR'] } },
  { path: 'carrito', component: CarritoComponent },
  { path: 'vendedor', component: VendedorComponent, canActivate: [AuthGuard], data: { expectedRoles: ['VENDEDOR'] } },
  { path: 'bodega', component: BodegueroComponent, canActivate: [AuthGuard], data: { expectedRoles: ['BODEGUERO'] } },
];

@NgModule({
  imports: [RouterModule.forRoot(appRoutes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
