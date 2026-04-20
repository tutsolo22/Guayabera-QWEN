import { api } from './api';

export interface CuentaContable {
  id: string;
  codigo: string;
  nombre: string;
  nivel: number;
  tipo: 'activo' | 'pasivo' | 'capital' | 'ingresos' | 'costos' | 'gastos';
  naturaleza?: 'deudora' | 'acreedora';
  es_cuenta_mayor: boolean;
  es_agrupadora: boolean;
  activa: boolean;
  descripcion?: string;
  cuenta_padre_id?: string;
  created_at: string;
}

export interface PolizaContable {
  id: string;
  numero: number;
  tipo: 'diario' | 'ingreso' | 'egreso';
  fecha: string;
  descripcion: string;
  estado: 'borrador' | 'revisada' | 'aprobada' | 'cancelada';
  total_cargos: number;
  total_abonos: number;
  esta_cuadrada: boolean;
  movimientos: MovimientoPoliza[];
  created_at: string;
}

export interface MovimientoPoliza {
  id: string;
  cuenta_id: string;
  cuenta?: CuentaContable;
  cargo: number;
  abono: number;
  concepto: string;
  referencia?: string;
}

export interface Banco {
  id: string;
  nombre: string;
  cuenta: string;
  clabe?: string;
  tipo_cuenta?: string;
  moneda: string;
  saldo_actual: number;
  activo: boolean;
  created_at: string;
}

export interface BalanzaComprobacion {
  fecha_desde: string;
  fecha_hasta: string;
  lineas: BalanzaLinea[];
  total_cargos: number;
  total_abonos: number;
  esta_cuadrada: boolean;
}

export interface BalanzaLinea {
  cuenta_id: string;
  cuenta_codigo: string;
  cuenta_nombre: string;
  nivel: number;
  tipo: string;
  saldo_inicial: number;
  cargos: number;
  abonos: number;
  saldo_final: number;
}

export const financeApi = api.injectEndpoints({
  endpoints: (builder) => ({
    // Cuentas contables
    getCuentas: builder.query<CuentaContable[], { tipo?: string; solo_mayor?: boolean } | void>({
      query: ({ tipo, solo_mayor } = {}) => {
        const params = new URLSearchParams();
        if (tipo) params.append('tipo', tipo);
        if (solo_mayor) params.append('solo_mayor', 'true');
        return `/finance/cuentas?${params.toString()}`;
      },
      providesTags: ['Cuenta'],
    }),
    createCuenta: builder.mutation<CuentaContable, Partial<CuentaContable>>({
      query: (cuenta) => ({
        url: '/finance/cuentas',
        method: 'POST',
        body: cuenta,
      }),
      invalidatesTags: ['Cuenta'],
    }),
    importarCatalogoSAT: builder.mutation<{ cuentas_importadas: number }, void>({
      query: () => ({
        url: '/finance/cuentas/importar-sat',
        method: 'POST',
      }),
      invalidatesTags: ['Cuenta'],
    }),

    // Pólizas contables
    getPolizas: builder.query<PolizaContable[], { fecha_desde?: string; fecha_hasta?: string; tipo?: string; estado?: string } | void>({
      query: ({ fecha_desde, fecha_hasta, tipo, estado } = {}) => {
        const params = new URLSearchParams();
        if (fecha_desde) params.append('fecha_desde', fecha_desde);
        if (fecha_hasta) params.append('fecha_hasta', fecha_hasta);
        if (tipo) params.append('tipo', tipo);
        if (estado) params.append('estado', estado);
        return `/finance/polizas?${params.toString()}`;
      },
      providesTags: ['Poliza'],
    }),
    getPoliza: builder.query<PolizaContable, string>({
      query: (id) => `/finance/polizas/${id}`,
      providesTags: ['Poliza'],
    }),
    createPoliza: builder.mutation<PolizaContable, any>({
      query: (poliza) => ({
        url: '/finance/polizas',
        method: 'POST',
        body: poliza,
      }),
      invalidatesTags: ['Poliza'],
    }),

    // Bancos
    getBancos: builder.query<Banco[], void>({
      query: () => '/finance/bancos',
      providesTags: ['Banco'],
    }),
    createBanco: builder.mutation<Banco, Partial<Banco>>({
      query: (banco) => ({
        url: '/finance/bancos',
        method: 'POST',
        body: banco,
      }),
      invalidatesTags: ['Banco'],
    }),

    // Balanza de comprobación
    getBalanzaComprobacion: builder.query<BalanzaComprobacion, { fecha_desde: string; fecha_hasta: string }>({
      query: ({ fecha_desde, fecha_hasta }) => ({
        url: '/finance/reportes/balanza-comprobacion',
        method: 'POST',
        body: { fecha_desde, fecha_hasta },
      }),
    }),

    // Asientos automáticos
    getAsientosAutomaticos: builder.query({
      query: (params: { modulo_origen?: string; estado?: string } | void = {}) => {
        const searchParams = new URLSearchParams();
        if (params && typeof params === 'object' && 'modulo_origen' in params && params.modulo_origen) {
          searchParams.append('modulo_origen', params.modulo_origen);
        }
        if (params && typeof params === 'object' && 'estado' in params && params.estado) {
          searchParams.append('estado', params.estado);
        }
        return `/finance/automaticos/monitoreo?${searchParams.toString()}`;
      },
      providesTags: ['AsientoAutomatico'],
    }),
    getAsientosEstadisticas: builder.query({
      query: () => '/finance/automaticos/estadisticas',
    }),
  }),
});

export const {
  useGetCuentasQuery,
  useCreateCuentaMutation,
  useImportarCatalogoSATMutation,
  useGetPolizasQuery,
  useGetPolizaQuery,
  useCreatePolizaMutation,
  useGetBancosQuery,
  useCreateBancoMutation,
  useGetBalanzaComprobacionQuery,
  useGetAsientosAutomaticosQuery,
  useGetAsientosEstadisticasQuery,
} = financeApi;
