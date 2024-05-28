import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { AdminService } from '../../../services/admin.service';
import { User } from '../../interfaces/user';

@Component({
  selector: 'propilot-admin',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.scss',
})

export class AdminComponent implements OnInit {
  users: User[] = [];
  userId: number = 0;

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
      },
      (error) => {
        console.error('Error al obtener usuario:', error);
      }
    );
  }
}
