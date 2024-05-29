import { CommonModule } from '@angular/common';
import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../../services/product.service';
import { Product } from '../../interfaces/product';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'propilot-vendedor',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './vendedor.component.html',
  styleUrl: './vendedor.component.scss',
})
export class VendedorComponent implements OnInit {
  products: Product[] = [];
  selectedProduct: Product | null = null;
  
  initialProductState: Product = {
    id: '',
    name: '',
    brand: '',
    image: null,
    price: [{
      date: new Date().toISOString(),
      price: 0
    }],
    enabled: true,
    modified_date: new Date().toISOString(),
    stock: 0,
    category: '',
    created_date: new Date().toISOString(),
    deleted_date: null
  };

  newProduct: Product = { ...this.initialProductState };

  constructor(private productService: ProductService) {}

  ngOnInit(): void {
    this.loadProducts();
  }

  loadProducts(): void {
    this.productService.getProducts().subscribe(products => {
      this.products = products;
    });
  }

  editProduct(product: Product): void {
    this.selectedProduct = { ...product};
  }

  deleteProduct(id: string): void {
    this.productService.deleteProduct(id).subscribe(() => {
      this.loadProducts();
    })
  }

  saveProduct(): void {
    if (this.selectedProduct) {
      if (this.selectedProduct.id) {
        this.productService.updateProduct(this.selectedProduct.id, this.selectedProduct).subscribe(() => {
          this.loadProducts();
          this.selectedProduct = null;
        });
      } else {
        this.productService.createProduct(this.selectedProduct).subscribe(() => {
          this.loadProducts();
          this.selectedProduct = null;
        });
      }
    }
  }

  createProduct(): void {
    // Verifica que los campos obligatorios no estén vacíos y que el precio tenga al menos un elemento con un precio definido
    if (this.newProduct.name && this.newProduct.brand && this.newProduct.category) {
      this.productService.createProduct(this.newProduct).subscribe({
        next: () => {
          this.loadProducts(); // Recarga la lista de productos
          this.newProduct = { ...this.initialProductState }; // Restablece el formulario a su estado inicial
        },
        error: (error) => {
          console.error('Error al crear el producto:', error);
        }
      });
    } else {
      console.error('Los campos name, brand, price y category son obligatorios');
    }
  }
}
