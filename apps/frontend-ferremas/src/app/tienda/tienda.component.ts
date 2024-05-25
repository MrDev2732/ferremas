import { Injectable, Inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Product } from '../interfaces/product';

import {ENV, Environment} from "../../enviroments/enviroment.dev";

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
