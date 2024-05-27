export interface Producto {
    id: string;
    name: string;
    marca: string;
    imagen: string | null;
    precios: {
        fecha: string;
        valor: number;
    }[];
    enabled: boolean;
    modified_date: string;
    stock: number;
    categoria: string;
    created_date: string;
    deleted_date: string | null;
}
