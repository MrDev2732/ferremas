import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../../services/product-list.service'; // Importa el servicio
import { Product } from '../../interfaces/product'; // Importa la interfaz Product

@Component({
  selector: 'propilot-tienda',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tienda.component.html',
  styleUrl: './tienda.component.scss',
})
export class TiendaComponent implements OnInit {
  products: Product[] = [];
  valorDolar: number = 0;

  constructor(private productService: ProductService) {} // Inyecta el servicio

  ngOnInit(): void {
    this.productService.getProducts().subscribe((data: Product[]) => {
      this.products = data;
    });

    this.productService.getDolar().subscribe((data: number) => {
      this.valorDolar = data;
    });
  }


}



