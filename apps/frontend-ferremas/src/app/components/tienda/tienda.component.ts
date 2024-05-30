import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../../services/product-list.service'; // Importa el servicio
import { Product } from '../../interfaces/product'; // Importa la interfaz Product
import { CarritoService } from '../../../services/carrito.service'


@Component({
  selector: 'app-tienda',
  templateUrl: './tienda.component.html',
  styleUrls: ['./tienda.component.scss'],
})

export class TiendaComponent implements OnInit {
  products: Product[] = [];
  valorDolar: number = 0;

  constructor(private productService: ProductService, private carritoService: CarritoService) {} // Inyecta el servicio
  
  ngOnInit(): void {
    this.productService.getProducts().subscribe((data: Product[]) => {
      this.products = data;
    });

    this.productService.getDolar().subscribe((data: number) => {
      this.valorDolar = data;
    });
  }

  addToCart(product: Product) {
    this.carritoService.addToCart(product);
  }
}




