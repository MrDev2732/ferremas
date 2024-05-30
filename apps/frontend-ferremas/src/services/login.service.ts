import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { User } from '../app/interfaces/user'
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class LoginService {
  private apiUrl = 'http://localhost:8000/login';


  constructor(private http: HttpClient,
              private router: Router
  ) {}

  getUser(username: string, password: string) {
    return this.http.get(`${this.apiUrl}?username=${username}&password=${password}`);
  }

  logout(): void {
    localStorage.removeItem('userRole');
    localStorage.removeItem('userPassword');
    localStorage.removeItem('user');
    this.router.navigate(['/login']); // Redirige al usuario a la página de inicio de sesión
  }

}


