export interface Product {
    id: string;
    name: string;
    brand: string;
    image: string | null;
    price: {
        date: string;
        price: number;
    }[];
    enabled: boolean;
    modified_date: string;
    stock: number;
    category: string;
    created_date: string;
    deleted_date: string | null;
}
