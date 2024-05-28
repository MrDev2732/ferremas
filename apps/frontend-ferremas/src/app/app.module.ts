import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule } from '@angular/router';
import { HttpClientModule } from '@angular/common/http'; // Importa HttpClientModule
import { AppComponent } from './app.component';
import { appRoutes } from './app.routes';
import { HomeComponent } from './components/home/home.component';
import { TiendaComponent } from './components/tienda/tienda.component';


@NgModule({
  declarations: [AppComponent, HomeComponent, TiendaComponent],
  imports: [
    BrowserModule,
    RouterModule.forRoot(appRoutes, { initialNavigation: 'enabledBlocking' }),
    HttpClientModule, // Añade HttpClientModule a los imports
    
  ],
  providers: [],
  bootstrap: [AppComponent],
})
export class AppModule {}
