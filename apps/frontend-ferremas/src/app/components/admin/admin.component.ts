import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms'; // Importar FormsModule aquí
import { AdminService } from '../../../services/admin.service';
import { User } from '../../interfaces/user';

@Component({
  selector: 'propilot-admin',
  standalone: true,
  imports: [CommonModule, FormsModule], // Añadir FormsModule aquí
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss'],
})

export class AdminComponent implements OnInit {
  users: User[] = [];
  userId: number = 0;
  newUser: User = {id: 0, name: '', password: '', rol: ''};
  userFound: boolean = false;
  editingUserId: number | null = null; // Añadir esta línea

  constructor(private adminService: AdminService) {}

  ngOnInit() {
    this.adminService.getUsers().subscribe((data: User[]) => {
      this.users = data;
    });   
  }

  deleteUser(userId: number): void {
    this.adminService.deleteUser(userId).subscribe(
      (response) => {
        console.log('Respuesta del servidor:', response);

        window.location.reload();
      },
      (error) => {
        console.error('Error al obtener usuario:', error);
      }
    );
  }

  createUser(name: string, password: string, rol: string): void {
    const newUser: User = { id: 0, name, password, rol }; // Asumiendo que el id se genera en el backend
    this.adminService.createUser(newUser).subscribe({
      next: (response) => {
        console.log(response.message);
        // Aquí puedes agregar lógica adicional, como actualizar la lista de usuarios.
        window.location.reload();
      },
      error: (error) => {
        console.error('Error al crear el usuario:', error);
      }
    });
  }

  updateUser(userId: number, user: User): void {
    this.adminService.updateUser(userId, user).subscribe({
      next: (response) => {
        console.log('Usuario actualizado:', response.detail);
        // Aquí puedes agregar lógica adicional, como actualizar la lista de usuarios sin recargar la página.
      },
      error: (error) => {
        console.error('Error al actualizar el usuario:', error);
      }
    });
  }

  resetUser(): void {
    this.newUser = { id: 0, name: '', password: '', rol: '' };
  }

}
