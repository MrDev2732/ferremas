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
      const expectedRoles = next.data['expectedRoles'] as string[];
      const userRole = this.getUserRole();

      if (expectedRoles.includes(userRole)) {
        return true;
      } else {
        this.router.navigate(['/login']); // Redirige a login si no cumple con los roles
        return false;
      }
  }

  private getUserRole(): string {
    return localStorage.getItem('userRole') || 'defaultRole';
  }
}
