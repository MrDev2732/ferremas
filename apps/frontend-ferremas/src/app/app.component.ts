import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';


@Component({
  selector: 'ferremas-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'frontend-ferremas';
  userRole = '';
  
  constructor(private loginService: LoginService) { }


  logout(): void {
    localStorage.setItem('isLoged', 'false')
    this.loginService.logout();
  }

  isUserLoggedIn(): boolean {
    const isLoged = localStorage.getItem('isLoged');
    return isLoged === 'true'; // Devuelve true si isLoged es 'true', de lo contrario, devuelve false
  }
}
