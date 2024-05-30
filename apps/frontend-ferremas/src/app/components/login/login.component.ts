import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { LoginService } from '../../../services/login.service'; // Importa el servicio
import { User } from '../../../app/interfaces/user';
import { Router } from '@angular/router';


@Component({
  selector: 'propilot-login',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './login.component.html',
  styleUrl: './login.component.scss',
})
export class LoginComponent {
  constructor(private loginService: LoginService,
              private router: Router
  ) {}

/*   // Utilizar la función getUser del servicio LoginService
  loginUser(username: string, password: string): void {
    this.loginService.getUser(username, password).subscribe(
      (response) => {
        console.log('Respuesta del servidor:', response);
      },
      (error) => {
        console.error('Error al obtener usuario:', error);
      }
    );
  } */

  loginUser(username: string, password: string): void {
    this.loginService.getUser(username, password).subscribe(
      (response: any) => {
        // Extraer la información del usuario y su rol
        const { name, rol } = response;
        console.log('Usuario:', username);
        console.log('Rol:', rol);
  
        // Redirigir según el rol del usuario
        switch (rol) {
          case 'admin':
            this.router.navigate(['/admin']);
            break;
          case 'VENDEDOR':
            this.router.navigate(['/vendedor']);
            break;
          case 'BODEGUERO':
            this.router.navigate(['/bodega']);
            break;
          // Agrega casos para otros roles si es necesario
          default:
            // Si el rol no coincide con ninguno de los casos anteriores, manejar el escenario apropiadamente
            console.error('Rol no reconocido:', rol);
            // Por ejemplo, redirigir a una página de error o mostrar un mensaje al usuario
        }
      },
      (error) => {
        console.error('Error al obtener usuario:', error);
      }
    );
  }
  
}