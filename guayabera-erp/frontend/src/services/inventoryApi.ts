import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

interface BusquedaProductoTextil {
  modelo?: string;
  color?: string;
  talla?: string;
  almacen_id?: string;
  empresa_id?: string;
  categoria_producto?: string;
  codigo_producto?: string;
  nombre_producto?: string;
  sobrenombre_1?: string;
  sobrenombre_2?: string;
}

interface ResultadoBusquedaProducto {
  producto_id: string;
  codigo_producto: string;
  nombre_producto: string;
  modelo?: string;
  color?: string;
  talla?: string;
  almacen_id: string;
  almacen_nombre: string;
  empresa_id?: string;
  empresa_nombre?: string;
  cantidad_disponible: number;
  categoria_producto?: string;
  sobrenombre_1?: string;
  sobrenombre_2?: string;
}

interface ResultadoBusquedaAvanzada {
  resultados: ResultadoBusquedaProducto[];
  total_resultados: number;
  almacen_solicitud?: string;
  otros_almacenes_disponibles: Record<string, any>[];
}

export const inventoryApi = {
  buscarProductosTextilesAvanzada: async (busqueda: BusquedaProductoTextil): Promise<ResultadoBusquedaAvanzada> => {
    const response = await axios.post(`${API_BASE_URL}/inventory/buscar-productos-avanzada`, busqueda);
    return response.data;
  }
};