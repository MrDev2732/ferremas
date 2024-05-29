import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CarritoService {
  private apiUrl = 'http://localhost:8000/api'; // Asegúrate de que la URL coincida con la de tu servidor backend

  constructor(private http: HttpClient) { }

  createPayment() {
    return this.http.post('http://localhost:8000/create-payment', {});
  }
}