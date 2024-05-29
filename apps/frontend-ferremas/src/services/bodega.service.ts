import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})

export class BodegaService {

  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getProduct(): Observable<any> {
    return this.http.get(`${this.apiUrl}/get-products`);
  }

  updateStock(productId: string, stock: number): Observable<{"detail": "Producto actualizado exitosamente"}> {
    return this.http.put<{"detail": "Producto actualizado exitosamente"}>(`${this.apiUrl}/update-product?product_id=${productId}&stock=${stock}`, {});
 }
}
