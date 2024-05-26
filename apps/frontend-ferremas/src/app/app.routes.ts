import { Route } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { tiendaComponent } from './tienda/tienda.component';



export const appRoutes: Route[] = [
    {
     path: '', component: HomeComponent
    },
    {
    path: 'tienda', component: tiendaComponent
    },
];
