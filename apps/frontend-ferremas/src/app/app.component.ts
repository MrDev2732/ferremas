import { Component } from '@angular/core';
import { LoginService } from '../services/login.service';


@Component({
  selector: 'ferremas-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'frontend-ferremas';
  
  constructor(private loginService: LoginService) { }


  logout(): void {
    this.loginService.logout();
  }
}
