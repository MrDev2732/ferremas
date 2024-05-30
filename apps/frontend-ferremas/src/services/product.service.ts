import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../app/interfaces/product';


@Injectable({
  providedIn: 'root'
})


export class ProductService {
  private apiUrl = 'http://localhost:8000';
  private apiUrlDolar = 'http://localhost:8000/get-dolar';

  constructor(private http: HttpClient) { }

  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.apiUrl}/get-products`);
  }

  getProduct(id: string): Observable<Product> {
    return this.http.get<Product>(`${this.apiUrl}/get-product/${id}`);
  }

  getDolar(): Observable<any> {
    return this.http.get<any>(this.apiUrlDolar);
  }

  createProduct(formData: FormData): Observable<{message: string}> {
    return this.http.post<{message: string}>(`${this.apiUrl}/create-product`, formData);
  }

  updateProduct(id: string, product: Product): Observable<Product> {
    return this.http.put<Product>(`${this.apiUrl}/update-product${id}`, product);
  }

  deleteProduct(id: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/delete-product?product_id=${id}`);
  }
}
