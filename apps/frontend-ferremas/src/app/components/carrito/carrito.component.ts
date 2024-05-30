import { Component } from '@angular/core';
import { CarritoService } from '../../../services/carrito.service';
import { CommonModule } from '@angular/common';
// import { PaymentService } from '../../../services/payment.service';

@Component({
  selector: 'propilot-carrito',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carrito.component.html',
  styleUrls: ['./carrito.component.scss']
})
export class CarritoComponent {
  total: number = 500;

  constructor(private carritoService: CarritoService) {}

  makePayment() {
    this.carritoService.createPayment(this.total).subscribe((response: any) => {
      window.location.href = response.approval_url;
    }, error => {
      console.error('Error creating the payment: ', error);
    });
  }


}