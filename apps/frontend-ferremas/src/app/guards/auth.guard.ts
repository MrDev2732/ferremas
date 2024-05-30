import { CanActivate, ActivatedRouteSnapshot, RouterStateSnapshot, Router } from '@angular/router';
import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {
  constructor(private router: Router) {}

  canActivate(
    next: ActivatedRouteSnapshot,
    state: RouterStateSnapshot): boolean {
      const expectedRole = next.data['expectedRole'];
      const userRole = this.getUserRole(); // Implementa esta función según tu lógica de autenticación

      if (userRole === expectedRole) {
        return true;
      } else {
        this.router.navigate(['/login']); // Redirige a una página de no autorizado o a login
        return false;
      }
  }

  private getUserRole(): string {
    // Retorna un valor predeterminado si 'userRole' es null
    return localStorage.getItem('userRole') || 'defaultRole';
  }
}
