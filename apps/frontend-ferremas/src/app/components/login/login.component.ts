import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../../services/login.service'; // Importa el servicio
import { User } from '../../../app/interfaces/user';

@Component({
  selector: 'propilot-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  constructor(private loginService: LoginService) {}

  // Utilizar la función getUser del servicio LoginService
  loginUser(username: string, password: string): void {
    this.loginService.getUser(username, password).subscribe(
      (response) => {
        console.log('Respuesta del servidor:', response);
      },
      (error) => {
        console.error('Error al obtener usuario:', error);
      }
    );
  }
}