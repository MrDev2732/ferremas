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
}
