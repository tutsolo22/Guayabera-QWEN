/**
 * Supply Chain API Service
 * Handles suppliers, products, inventory, warehouses, and purchase orders
 */

import api from './api';

export interface Proveedor {
  id: string;
  codigo: string;
  nombre_comercial: string;
  razon_social?: string;
  rfc: string;
  correo_electronico?: string;
  telefono?: string;
  tipo_proveedor: 'nacional' | 'extranjero' | 'cliente_proveedor';
  activo: boolean;
  created_at: string;
}

export interface Producto {
  id: string;
  codigo: string;
  nombre: string;
  descripcion?: string;
  clave_sat?: string;
  costo_promedio: number;
  precio_venta_base: number;
  stock_minimo: number;
  cantidad_disponible?: number;
  activo: boolean;
}

export interface Almacen {
  id: string;
  codigo: string;
  nombre: string;
  descripcion?: string;
  ciudad?: string;
  estado?: string;
  tipo: string;
  es_principal: boolean;
  activo: boolean;
}

export interface OrdenCompra {
  id: string;
  folio: string;
  proveedor_id: string;
  fecha_emision: string;
  estado: 'borrador' | 'autorizada' | 'en_proceso' | 'parcialmente_recibida' | 'completada' | 'cancelada';
  subtotal: number;
  total: number;
  moneda: string;
  created_at: string;
  proveedor?: Proveedor;
}

export interface Inventario {
  id: string;
  producto_id: string;
  almacen_id: string;
  cantidad_disponible: number;
  cantidad_reservada: number;
  costo_promedio: number;
  producto?: Producto;
  almacen?: Almacen;
}

const supplyChainApi = {
  // ============= PROVEEDORES =============
  
  getProveedores: async (activo: boolean = true): Promise<Proveedor[]> => {
    const response = await api.get(`/supply-chain/proveedores?activo=${activo}`);
    return response.data;
  },

  getProveedor: async (id: string): Promise<Proveedor> => {
    const response = await api.get(`/supply-chain/proveedores/${id}`);
    return response.data;
  },

  createProveedor: async (data: Partial<Proveedor>): Promise<Proveedor> => {
    const response = await api.post('/supply-chain/proveedores', data);
    return response.data;
  },

  updateProveedor: async (id: string, data: Partial<Proveedor>): Promise<Proveedor> => {
    const response = await api.put(`/supply-chain/proveedores/${id}`, data);
    return response.data;
  },

  deleteProveedor: async (id: string): Promise<void> => {
    await api.delete(`/supply-chain/proveedores/${id}`);
  },

  // ============= PRODUCTOS =============
  
  getProductos: async (activo: boolean = true, categoria_id?: string): Promise<Producto[]> => {
    const params = new URLSearchParams({ activo: String(activo) });
    if (categoria_id) params.append('categoria_id', categoria_id);
    const response = await api.get(`/supply-chain/productos?${params}`);
    return response.data;
  },

  getProducto: async (id: string): Promise<Producto> => {
    const response = await api.get(`/supply-chain/productos/${id}`);
    return response.data;
  },

  createProducto: async (data: Partial<Producto>): Promise<Producto> => {
    const response = await api.post('/supply-chain/productos', data);
    return response.data;
  },

  updateProducto: async (id: string, data: Partial<Producto>): Promise<Producto> => {
    const response = await api.put(`/supply-chain/productos/${id}`, data);
    return response.data;
  },

  deleteProducto: async (id: string): Promise<void> => {
    await api.delete(`/supply-chain/productos/${id}`);
  },

  // ============= ALMACENES =============
  
  getAlmacenes: async (activo: boolean = true): Promise<Almacen[]> => {
    const response = await api.get(`/supply-chain/almacenes?activo=${activo}`);
    return response.data;
  },

  getAlmacen: async (id: string): Promise<Almacen> => {
    const response = await api.get(`/supply-chain/almacenes/${id}`);
    return response.data;
  },

  createAlmacen: async (data: Partial<Almacen>): Promise<Almacen> => {
    const response = await api.post('/supply-chain/almacenes', data);
    return response.data;
  },

  updateAlmacen: async (id: string, data: Partial<Almacen>): Promise<Almacen> => {
    const response = await api.put(`/supply-chain/almacenes/${id}`, data);
    return response.data;
  },

  // ============= INVENTARIOS =============
  
  getInventarios: async (almacen_id?: string): Promise<Inventario[]> => {
    const params = new URLSearchParams();
    if (almacen_id) params.append('almacen_id', almacen_id);
    const response = await api.get(`/supply-chain/inventarios?${params}`);
    return response.data;
  },

  getInventarioBajoStock: async (): Promise<Inventario[]> => {
    const response = await api.get('/supply-chain/inventarios/bajo-stock');
    return response.data;
  },

  // ============= ÓRDENES DE COMPRA =============
  
  getOrdenesCompra: async (
    proveedor_id?: string,
    estado?: string
  ): Promise<OrdenCompra[]> => {
    const params = new URLSearchParams();
    if (proveedor_id) params.append('proveedor_id', proveedor_id);
    if (estado) params.append('estado', estado);
    const response = await api.get(`/supply-chain/ordenes-compra?${params}`);
    return response.data;
  },

  getOrdenCompra: async (id: string): Promise<OrdenCompra> => {
    const response = await api.get(`/supply-chain/ordenes-compra/${id}`);
    return response.data;
  },

  createOrdenCompra: async (data: any): Promise<OrdenCompra> => {
    const response = await api.post('/supply-chain/ordenes-compra', data);
    return response.data;
  },

  updateEstadoOrden: async (id: string, estado: string): Promise<OrdenCompra> => {
    const response = await api.put(`/supply-chain/ordenes-compra/${id}/estado?estado=${estado}`);
    return response.data;
  },

  // ============= DASHBOARD =============
  
  getDashboardInventario: async (): Promise<any> => {
    const response = await api.get('/supply-chain/dashboard/inventario');
    return response.data;
  },

  getDashboardCompras: async (): Promise<any> => {
    const response = await api.get('/supply-chain/dashboard/compras');
    return response.data;
  },
};

export default supplyChainApi;
