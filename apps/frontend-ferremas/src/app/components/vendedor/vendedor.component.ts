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
    image: '',
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

  selectedFile: File | null = null;

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



  createProduct(): void {
    if (this.newProduct.name && this.newProduct.brand && this.newProduct.category && this.selectedFile) {
      const formData = new FormData();
      formData.append('category', this.newProduct.category);
      formData.append('product', this.newProduct.name);
      formData.append('brand', this.newProduct.brand);
      formData.append('image', this.selectedFile);

      this.productService.createProduct(formData).subscribe({
        next: () => {
          this.loadProducts();
          this.newProduct = { ...this.initialProductState };
          this.selectedFile = null;
        },
        error: (error) => {
          console.error('Error al crear el producto:', error);
        }
      });
    } else {
      console.error('Todos los campos y la imagen son obligatorios');
    }
  }

  onFileSelected(event: any): void {
    this.selectedFile = event.target.files[0];
  }
}
