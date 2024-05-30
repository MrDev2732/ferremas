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
  private readonly DOLAR_KEY = 'valorDolar';

  constructor(private productService: ProductService, private carritoService: CarritoService) {}

  ngOnInit(): void {
    this.productService.getProducts().subscribe((data: Product[]) => {
      this.products = data.map(product => ({
        ...product,
        image: product.image ? 'data:image/jpeg;base64,' + product.image : null
      }));
    });

    const cachedDolar = localStorage.getItem(this.DOLAR_KEY);
    if (cachedDolar) {
      this.valorDolar = parseFloat(cachedDolar);
    } else {
      this.productService.getDolar().subscribe((data: number) => {
        this.valorDolar = data;
        localStorage.setItem(this.DOLAR_KEY, data.toString());
      });
    }
  }

  addToCart(product: Product) {
    const added = this.carritoService.addToCart(product);
    if (!added) {
      alert('No se puede agregar mas de este producto, stock insuficiente.');
    }
  }
}
