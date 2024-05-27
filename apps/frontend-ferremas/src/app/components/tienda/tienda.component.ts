import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../../services/product-list.service'; // Importa el servicio
import { Producto } from '../../interfaces/producto'; // Importa la interfaz Producto

@Component({
  selector: 'propilot-tienda',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './tienda.component.html',
  styleUrl: './tienda.component.scss',
})
export class TiendaComponent implements OnInit {
  productos: Producto[] = [];

  constructor(private productService: ProductService) {} // Inyecta el servicio

  ngOnInit(): void {
    this.productService.getProducts().subscribe((data: Producto[]) => {
      this.productos = data;
    });
  }
}



