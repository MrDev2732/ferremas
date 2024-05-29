import { Component } from '@angular/core';
import { CarritoService } from '../../../services/carrito.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'propilot-carrito',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carrito.component.html',
  styleUrls: ['./carrito.component.scss']
})
export class CarritoComponent {
  constructor(private carritoService: CarritoService) {}

  makePayment() {
    this.carritoService.createPayment().subscribe((response: any) => {
      window.location.href = response.approval_url;
    }, error => {
      console.error('Error creating the payment: ', error);
    });
  }
}