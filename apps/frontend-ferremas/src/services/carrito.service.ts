import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../app/interfaces/product'

@Injectable({
  providedIn: 'root'
})

export class CarritoService {
  private apiUrl = 'http://localhost:8000'; // Asegúrate de que la URL coincida con tu servidor backend
  private cart: { product: Product, quantity: number }[] = [];

  constructor(private http: HttpClient) { }

  createPayment(total: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/create-payment?total=${total}`, {});  }


  addToCart(product: Product) {
    const existingProduct = this.cart.find(item => item.product.id === product.id);
    if (existingProduct) {
      existingProduct.quantity += 1;
    } else {
      this.cart.push({ product, quantity: 1 });
    }
  }
  
  getCart() {
    return this.cart;
  }
}