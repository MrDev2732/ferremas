import { Route } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { TiendaComponent } from './components/tienda/tienda.component';

export const appRoutes: Route[] = [
  { path: '', component: HomeComponent },
  { path: 'tienda', component: TiendaComponent },
];
