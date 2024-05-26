import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../interfaces/product';
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

import {ENV, Environment} from "../../enviroments/enviroment.dev";

@Component({
  selector: 'app-tienda',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tienda.component.html',
  styleUrl: './tienda.component.scss',
})
export class tiendaComponent {}

@Injectable({
  providedIn: 'root'
})
export class ConfigService {

  private configUrl!: string;

  constructor(private http: HttpClient,
              @Inject(ENV) private environment: Environment,) {
    this.configUrl = environment.apiUrl + 'obtener-productos'
  }
  getProducts( ): Observable<Product>{
    return this.http.get<Product>(`${this.configUrl}`)
  }

}

