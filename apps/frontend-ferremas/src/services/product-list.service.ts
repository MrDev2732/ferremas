import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../app/interfaces/product';


@Injectable({
  providedIn: 'root',
})

export class ProductService {
  private apiUrl = 'http://localhost:8000/get-products';
  private apiUrlDolar = 'http://localhost:8000/get-dolar';

  constructor(private http: HttpClient) {}

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(this.apiUrl);
  }

  getDolar(): Observable<any> {
    return this.http.get<any>(this.apiUrlDolar);
  }

  getProduct(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/get-product`);
  }

  getProductos(id: String): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/get-product/${id}`);
  }

  updateProduct(id: string, product: Product): Observable<Product>{
    return this.http.put<Product>(`${this.apiUrl}/update-product/${id}`, product);
  }

  deleteProduct(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/delete-product/${id}`);
  }
}