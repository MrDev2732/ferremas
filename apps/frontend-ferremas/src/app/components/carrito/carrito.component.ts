import { Component, OnInit } from '@angular/core';
import { CarritoService } from '../../../services/carrito.service';
import { CommonModule } from '@angular/common';
import { Product } from '../../interfaces/product'
import { ProductService } from 'apps/frontend-ferremas/src/services/product-list.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-carrito',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './carrito.component.html',
  styleUrls: ['./carrito.component.scss']
})
export class CarritoComponent {
  total: number = 0;
  valorDolar: number = 0;
  cart: { product: Product, quantity: number } [] = [];

  constructor(private carritoService: CarritoService, private productService: ProductService, private router: Router) {
    this.cart = this.carritoService.getCart();
  }

  ngOnInit(): void {
    this.productService.getDolar().subscribe((data: number) => {
      this.valorDolar = data;
    });
  }

  getTotal(): number {
    return this.cart.reduce((total, item) => {
      return total + item.product.price[0].price * item.quantity * this.valorDolar;
    }, 0);
  }

  removeFromCart(productId: string) {
    this.carritoService.removeFromCart(productId);
    this.cart = this.carritoService.getCart();
  }

  makePayment() {
    this.total = this.getTotal();
    this.carritoService.createPayment(this.total).subscribe((response: any) => {
      window.location.href = response.approval_url;
    }, error => {
      console.error('Error creating the payment: ', error);
    });
  }

  goToShop() {
    this.router.navigate(['/tienda']); // Ajusta la ruta según tu configuración
  }
}