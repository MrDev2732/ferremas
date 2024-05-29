import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { BodegaService } from 'apps/frontend-ferremas/src/services/bodega.service';
import { Product } from '../../interfaces/product';

@Component({
  selector: 'app-bodeguero',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './bodeguero.component.html',
  styleUrl: './bodeguero.component.scss',
})

export class BodegueroComponent implements OnInit {

  products: Product[] = [];
  selectedProduct: Product | null = null;
  editingProductId: string | null = null;

  constructor(private bodegaService: BodegaService) { }

  ngOnInit(): void {
    this.loadStock();
  }

  loadStock(): void {
    this.bodegaService.getProduct().subscribe((data: Product[]) => {
      this.products = data;
    });
  }

  updateProduct(product: Product): void {
    this.bodegaService.updateStock(product.id, product.stock).subscribe({
      next: (response: any) => {
        console.log('Producto actualizado:', response.detail);
        this.editingProductId = null;  // Resetear el ID de edición al guardar
  
        // Encuentra el producto en la lista y actualiza su stock
        const index = this.products.findIndex(p => p.id === product.id);
        if (index !== -1) {
          this.products[index].stock = product.stock;
        }
      },
      error: (error: any) => {
        console.error('Error al actualizar el producto:', error);
      }
    });
  }
}

