import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Producto } from '../app/interfaces/producto';


@Injectable({
  providedIn: 'root',
})
export class ProductService {
  private apiUrl = 'http://localhost:8000/obtener-productos';

  constructor(private http: HttpClient) {}

  getProducts(): Observable<Producto[]> {
    return this.http.get<Producto[]>(this.apiUrl);
  }

  getProductByCode(productCode: string): Observable<Producto> {
    return this.http.get<Producto>(`${this.apiUrl}/${productCode}`);
  }

  addProduct(formData: FormData): Observable<any> {
    return this.http.post<any>(this.apiUrl, formData);
  }

}