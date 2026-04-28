import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Progress, DatePicker, Select, Tooltip } from 'antd';
import { 
  DollarOutlined, 
  TeamOutlined, 
  ShoppingCartOutlined, 
  StockOutlined, 
  FileTextOutlined, 
  RiseOutlined,
  FallOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
  ExclamationCircleOutlined,
  UserOutlined,
  CalendarOutlined,
  PieChartOutlined,
  LineChartOutlined,
  BarChartOutlined
} from '@ant-design/icons';
import { Line, Column, Pie } from '@antv/plots';

const { Title, Text } = Typography;
const { Option } = Select;
const { RangePicker } = DatePicker;

const ExecutiveDashboard: React.FC = () => {
  const [dateRange, setDateRange] = useState<any>(null);
  const [period, setPeriod] = useState<string>('month');
  
  // Datos simulados para KPIs
  const kpiData = [
    { key: 'ventas', title: 'Ventas', value: 1250000, prevValue: 1100000, isPositive: true },
    { key: 'costos', title: 'Costos', value: 750000, prevValue: 720000, isPositive: false },
    { key: 'utilidad', title: 'Utilidad Neta', value: 500000, prevValue: 380000, isPositive: true },
    { key: 'empleados', title: 'Empleados', value: 124, prevValue: 120, isPositive: true },
  ];
  
  // Datos para gráfico de tendencias
  const trendData = [
    { month: 'Ene', ventas: 1000000, costos: 600000, utilidad: 400000 },
    { month: 'Feb', ventas: 1100000, costos: 650000, utilidad: 450000 },
    { month: 'Mar', ventas: 1200000, costos: 700000, utilidad: 500000 },
    { month: 'Abr', ventas: 1250000, costos: 750000, utilidad: 500000 },
    { month: 'May', ventas: 1300000, costos: 780000, utilidad: 520000 },
    { month: 'Jun', ventas: 1350000, costos: 800000, utilidad: 550000 },
  ];
  
  // Datos para distribución de empleados por departamento
  const deptData = [
    { name: 'TI', count: 12, percentage: 10 },
    { name: 'Finanzas', count: 8, percentage: 6 },
    { name: 'Producción', count: 45, percentage: 36 },
    { name: 'Ventas', count: 22, percentage: 18 },
    { name: 'Recursos Humanos', count: 15, percentage: 12 },
    { name: 'Logística', count: 10, percentage: 8 },
    { name: 'Calidad', count: 12, percentage: 10 },
  ];
  
  // Datos para órdenes de compra pendientes
  const purchaseOrdersData = [
    { key: '1', folio: 'OC-2023-001', proveedor: 'Proveedor ABC', total: 45000, status: 'pending', fecha: '2023-04-15' },
    { key: '2', folio: 'OC-2023-002', proveedor: 'Proveedor XYZ', total: 32000, status: 'approved', fecha: '2023-04-16' },
    { key: '3', folio: 'OC-2023-003', proveedor: 'Proveedor DEF', total: 28000, status: 'pending', fecha: '2023-04-17' },
    { key: '4', folio: 'OC-2023-004', proveedor: 'Proveedor GHI', total: 56000, status: 'delivered', fecha: '2023-04-18' },
  ];
  
  // Datos para facturas pendientes
  const invoicesData = [
    { key: '1', folio: 'FAC-2023-001', cliente: 'Cliente A', total: 25000, vencimiento: '2023-04-25', status: 'pending' },
    { key: '2', folio: 'FAC-2023-002', cliente: 'Cliente B', total: 18000, vencimiento: '2023-04-20', status: 'overdue' },
    { key: '3', folio: 'FAC-2023-003', cliente: 'Cliente C', total: 32000, vencimiento: '2023-05-02', status: 'pending' },
    { key: '4', folio: 'FAC-2023-004', cliente: 'Cliente D', total: 15000, vencimiento: '2023-04-18', status: 'paid' },
  ];
  
  const columnasOrdenesCompra = [
    { title: 'Folio', dataIndex: 'folio', key: 'folio' },
    { title: 'Proveedor', dataIndex: 'proveedor', key: 'proveedor' },
    { title: 'Total', dataIndex: 'total', key: 'total', render: (total: number) => `$${total.toLocaleString()}` },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => {
        let color = 'default';
        if (status === 'pending') color = 'orange';
        if (status === 'approved') color = 'blue';
        if (status === 'delivered') color = 'green';
        return <Tag color={color}>{status}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
          <Button type="link">Aprobar</Button>
        </Space>
      ),
    },
  ];
  
  const columnasFacturas = [
    { title: 'Folio', dataIndex: 'folio', key: 'folio' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { title: 'Total', dataIndex: 'total', key: 'total', render: (total: number) `$${total.toLocaleString()}` },
    { 
      title: 'Status', 
      dataIndex: 'status', 
      key: 'status',
      render: (status: string) => {
        let color = 'default';
        if (status === 'pending') color = 'orange';
        if (status === 'overdue') color = 'red';
        if (status === 'paid') color = 'green';
        return <Tag color={color}>{status}</Tag>;
      }
    },
    { title: 'Vencimiento', dataIndex: 'vencimiento', key: 'vencimiento' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
          <Button type="link">Cobrar</Button>
        </Space>
      ),
    },
  ];
  
  // Configuración para gráficos
  const trendConfig = {
    data: trendData,
    xField: 'month',
    yField: ['ventas', 'costos', 'utilidad'],
    seriesField: 'type',
    isGroup: true,
    columnWidthRatio: 0.4,
    dodgePadding: 2,
    legend: {
      position: 'top',
    },
    tooltip: {
      formatter: (datum: any) => {
        return { name: datum.type, value: `$${datum.value.toLocaleString()}` };
      },
    },
  };
  
  const pieConfig = {
    data: deptData,
    angleField: 'count',
    colorField: 'name',
    radius: 0.8,
    label: {
      type: 'outer',
      content: '{name} {percentage}',
    },
    interactions: [
      { type: 'element-selected' },
      { type: 'element-active' },
    ],
  };
  
  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Dashboard Ejecutivo</Title>
          <Text>
            Visión general del desempeño empresarial con KPIs y métricas clave
          </Text>
        </div>
        <Space>
          <Button>Exportar PDF</Button>
          <Button type="primary">Programar Reporte</Button>
        </Space>
      </Row>

      <Card style={{ marginBottom: 24 }}>
        <Row gutter={16} align="middle">
          <Col span={8}>
            <RangePicker 
              onChange={(dates) => setDateRange(dates as [moment.Moment | null, moment.Moment | null])} 
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={8}>
            <Select 
              defaultValue="all" 
              style={{ width: '100%' }}
            >
              <Option value="all">Todos los Departamentos</Option>
              <Option value="ventas">Ventas</Option>
              <Option value="produccion">Producción</Option>
              <Option value="finanzas">Finanzas</Option>
              <Option value="rh">Recursos Humanos</Option>
            </Select>
          </Col>
          <Col span={8} style={{ textAlign: 'right' }}>
            <Space>
              <Button>Comparar Periodos</Button>
              <Button type="primary">Actualizar Datos</Button>
            </Space>
          </Col>
        </Row>
      </Card>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Ventas Totales"
              value={1250000}
              precision={2}
              valueStyle={{ color: '#3f8600' }}
              prefix="$"
              suffix="MXN"
              suffixStyle={{ color: '#3f8600' }}
            />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 8 }}>
              <ArrowUpOutlined style={{ color: '#3f8600', marginRight: 4 }} />
              <span>12.5% desde el mes pasado</span>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Clientes Nuevos"
              value={125}
              valueStyle={{ color: '#1890ff' }}
            />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 8 }}>
              <ArrowUpOutlined style={{ color: '#1890ff', marginRight: 4 }} />
              <span>8.2% desde el mes pasado</span>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Productos Activos"
              value={245}
              valueStyle={{ color: '#cf1322' }}
            />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 8 }}>
              <ArrowUpOutlined style={{ color: '#cf1322', marginRight: 4 }} />
              <span>5 nuevos este mes</span>
            </div>
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Tasa de Retención"
              value={87.5}
              precision={2}
              valueStyle={{ color: '#722ed1' }}
              suffix="%"
            />
            <div style={{ display: 'flex', alignItems: 'center', marginTop: 8 }}>
              <ArrowDownOutlined style={{ color: '#722ed1', marginRight: 4 }} />
              <span>2.1% desde el mes pasado</span>
            </div>
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="overview" onChange={setActiveTab}>
        <TabPane tab="Resumen General" key="overview">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Evolución de Ventas" style={{ marginBottom: 16 }}>
                <Column {...columnConfig} height={300} />
              </Card>
              
              <Card title="Top Productos por Ingresos">
                <Table
                  dataSource={topProductsData}
                  columns={[
                    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
                    { title: 'Unidades Vendidas', dataIndex: 'vendidos', key: 'vendidos' },
                    { 
                      title: 'Ingresos', 
                      dataIndex: 'ingresos', 
                      key: 'ingresos',
                      render: (val) => `$${val.toLocaleString()}`
                    }
                  ]}
                  pagination={false}
                  size="small"
                />
              </Card>
            </Col>
            <Col span={8}>
              <Card title="KPIs Clave" style={{ marginBottom: 16 }}>
                <Table
                  dataSource={kpiData}
                  columns={[
                    { 
                      title: 'Nombre', 
                      dataIndex: 'nombre',
                      render: (text) => <Text strong>{text}</Text>
                    },
                    { 
                      title: 'Actual', 
                      dataIndex: 'valorActual',
                      render: (val, record) => (
                        <Text>{record.nombre.includes('Tiempo') ? `${val} días` : `$${val.toLocaleString()}`}</Text>
                      )
                    },
                    { 
                      title: 'Meta', 
                      dataIndex: 'meta',
                      render: (val, record) => (
                        <Text>{record.nombre.includes('Tiempo') ? `${val} días` : `$${val.toLocaleString()}`}</Text>
                      )
                    },
                    { 
                      title: 'Cambio', 
                      dataIndex: 'cambio',
                      render: (val, record) => (
                        <Text type={record.estado === 'success' ? 'success' : record.estado === 'error' ? 'danger' : 'warning'}>
                          {val}
                        </Text>
                      )
                    }
                  ]}
                  pagination={false}
                  size="small"
                />
              </Card>
              
              <Card title="Alertas">
                <div style={{ padding: '8px 0' }}>
                  <Text strong type="danger">Margen de ganancia bajo</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: '12px' }}>Actual: 25.5% vs Meta: 30%</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong type="danger">Tiempo de entrega superior al objetivo</Text>
                  <br />
                  <Text type="secondary" style={{ fontSize: '12px' }}>Actual: 3.2 días vs Meta: 2.5 días</Text>
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>
        
        <TabPane tab="Business Intelligence" key="bi">
          <Row gutter={16}>
            <Col span={8}>
              <Card 
                title={<><TrophyOutlined /> KPIs Clave</>} 
                style={{ marginBottom: 16 }}
                extra={<Button type="link" href="/business-intelligence/kpi">Ver más</Button>}
              >
                <div style={{ padding: '8px 0' }}>
                  <Text strong>Clientes Nuevos: </Text>
                  <Text>125 (Meta: 150)</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Ventas Totales: </Text>
                  <Text>$1,250,000</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Margen de Ganancia: </Text>
                  <Text>25.5% (Meta: 30%)</Text>
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card 
                title={<><ThunderboltOutlined /> Análisis Predictivo</>} 
                style={{ marginBottom: 16 }}
                extra={<Button type="link" href="/business-intelligence/predictive-analysis">Ver más</Button>}
              >
                <div style={{ padding: '8px 0' }}>
                  <Text strong>Predicción de Ventas Q3: </Text>
                  <Text>+15.2%</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Demanda de Productos: </Text>
                  <Text>Alta en temporada</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Retención de Clientes: </Text>
                  <Text>89.7%</Text>
                </div>
              </Card>
            </Col>
            <Col span={8}>
              <Card 
                title={<><BarChartOutlined /> Reportes Personalizados</>} 
                extra={<Button type="link" href="/reports/custom-reports">Ver más</Button>}
              >
                <div style={{ padding: '8px 0' }}>
                  <Text strong>Reportes Disponibles: </Text>
                  <Text>12</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Último Ejecutado: </Text>
                  <Text>Hace 2 horas</Text>
                </div>
                <div style={{ padding: '8px 0', borderTop: '1px solid #f0f0f0' }}>
                  <Text strong>Programados: </Text>
                  <Text>5</Text>
                </div>
              </Card>
            </Col>
          </Row>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default ExecutiveDashboard;