import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../../services/login.service';
import { Router } from '@angular/router';

@Component({
  selector: 'propilot-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  constructor(private loginService: LoginService, private router: Router) {}

  loginUser(username: string, password: string): void {
    this.loginService.getUser(username, password).subscribe(
      (response: any) => {
        const userRole = response.rol; 
        const userPassword = response.password
        const user = response.user// Changed from 'userRole' to 'rol'
        if (userRole) {
          localStorage.setItem('userRole', userRole);
          localStorage.setItem('userPassword', userPassword);
          localStorage.setItem('user', user) // Store user role
          this.redirectUser(userRole); // Redirect user based on role
        } else {
          console.error('User role not provided');
          this.router.navigate(['/login']); // Redirect to login if no role provided
        }
      },
      (error) => {
        console.error('Error getting user:', error);
        this.router.navigate(['/login']); // Redirect to login on error
      }
    );
  }

  private redirectUser(role: string): void {
    if (role) {
      switch (role.toUpperCase()) {
        case 'ADMINISTRADOR':
          this.router.navigate(['/admin']);
          break;
        case 'VENDEDOR':
          this.router.navigate(['/vendedor']);
          break;
        case 'BODEGUERO':
          this.router.navigate(['/bodega']);
          break;
        default:
          console.error('Unrecognized role:', role);
          this.router.navigate(['/login']); // Redirect to login if role not recognized
          break;
      }
    } else {
      console.error('Role undefined');
      this.router.navigate(['/login']); // Redirect to login if role is undefined
    }
  }
}
