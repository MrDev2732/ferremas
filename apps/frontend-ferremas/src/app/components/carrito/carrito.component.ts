import { Component, OnInit } from '@angular/core';
import { CarritoService } from '../../../services/carrito.service';
import { CommonModule } from '@angular/common';
import { Product } from '../../interfaces/product'

@Component({
  selector: 'app-carrito',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carrito.component.html',
  styleUrls: ['./carrito.component.scss']
})

export class CarritoComponent {
  total: number = 500;
  cart: Product[] = [];

  constructor(private carritoService: CarritoService) {
    this.cart = this.carritoService.getCart();
  }

  makePayment() {
    this.carritoService.createPayment(this.total).subscribe((response: any) => {
      window.location.href = response.approval_url;
    }, error => {
      console.error('Error creating the payment: ', error);
    });
  }
}