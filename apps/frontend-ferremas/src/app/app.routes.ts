import { Route } from '@angular/router';


export const appRoutes: Route[] = [
  {
    path: '',
    loadComponent: () => import("./components/home/home.component").then( m => m.HomeComponent)

  },
  {
    path: 'tienda',
    loadComponent: () => import("./components/tienda/tienda.component").then( m => m.TiendaComponent)

  }
];
