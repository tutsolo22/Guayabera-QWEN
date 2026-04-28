import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Button, Space, Typography, Statistic, Table, Tabs, DatePicker, Select, Modal, Form, Input, Tag } from 'antd';
import { 
  BarChartOutlined, 
  LineChartOutlined, 
  PieChartOutlined, 
  DashboardOutlined, 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  EyeOutlined,
  FilterOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { Column, ColumnConfig } from '@ant-design/plots';

const { Title, Text } = Typography;
const { RangePicker } = DatePicker;
const { TabPane } = Tabs;
const { Option } = Select;

const BusinessIntelligenceDashboard: React.FC = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dateRange, setDateRange] = useState<[moment.Moment | null, moment.Moment | null]>([null, null]);
  const [selectedDepartment, setSelectedDepartment] = useState<string>('all');

  // Datos simulados para las tablas
  const kpiData = [
    { id: '1', nombre: 'Ventas Totales', valorActual: 1250000, meta: 1500000, cambio: '+12.5%', estado: 'warning' },
    { id: '2', nombre: 'Clientes Nuevos', valorActual: 125, meta: 150, cambio: '+8.2%', estado: 'success' },
    { id: '3', nombre: 'Margen de Ganancia', valorActual: 25.5, meta: 30, cambio: '-2.1%', estado: 'error' },
    { id: '4', nombre: 'Tiempo Promedio de Entrega', valorActual: 3.2, meta: 2.5, cambio: '+0.3 días', estado: 'error' },
  ];

  const reportData = [
    { id: '1', nombre: 'Reporte de Ventas Mensual', tipo: 'ventas', autor: 'Juan Pérez', fecha: '2023-04-15' },
    { id: '2', nombre: 'Análisis de Costos', tipo: 'finanzas', autor: 'María López', fecha: '2023-04-14' },
    { id: '3', nombre: 'Eficiencia de Producción', tipo: 'producción', autor: 'Carlos Gómez', fecha: '2023-04-13' },
    { id: '4', nombre: 'Rotación de Personal', tipo: 'RH', autor: 'Ana Martínez', fecha: '2023-04-12' },
  ];

  const analysisData = [
    { id: '1', nombre: 'Predicción de Ventas Q3', modelo: 'Regresión Lineal', precisión: 92.5, ultima_ejecución: '2023-04-15' },
    { id: '2', nombre: 'Demanda de Productos', modelo: 'Series Temporales', precisión: 87.3, ultima_ejecución: '2023-04-14' },
    { id: '3', nombre: 'Retención de Clientes', modelo: 'Clasificación', precisión: 89.7, ultima_ejecución: '2023-04-13' },
  ];

  // Configuración de gráficos
  const salesData = [
    { month: 'Ene', ventas: 380000 },
    { month: 'Feb', ventas: 420000 },
    { month: 'Mar', ventas: 450000 },
    { month: 'Abr', ventas: 520000 },
    { month: 'May', ventas: 480000 },
    { month: 'Jun', ventas: 550000 },
  ];

  const productData = [
    { producto: 'Camisas', ventas: 35 },
    { producto: 'Pantalones', ventas: 28 },
    { producto: 'Vestidos', ventas: 18 },
    { producto: 'Chaquetas', ventas: 12 },
    { producto: 'Accesorios', ventas: 7 },
  ];

  const columnConfig: ColumnConfig = {
    data: salesData,
    xField: 'month',
    yField: 'ventas',
    color: '#1890FF',
    label: {
      position: 'top',
      style: {
        fill: '#FFFFFF',
        opacity: 0.6,
      },
    },
    xAxis: {
      label: {
        autoHide: true,
        autoRotate: false,
      },
    },
    meta: {
      ventas: {
        alias: 'Ventas ($)',
        formatter: (v) => `${(v / 1000).toFixed(0)}k`,
      },
    },
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><BarChartOutlined /> Business Intelligence</Title>
          <Text>
            Panel de control para análisis, reportes y toma de decisiones
          </Text>
        </div>
        <Space>
          <Button icon={<ReloadOutlined />}>Actualizar Datos</Button>
          <Button icon={<PlusOutlined />}>Nuevo Reporte</Button>
        </Space>
      </Row>

      <Card style={{ marginBottom: 24 }}>
        <Row gutter={16} align="middle">
          <Col span={6}>
            <FilterOutlined style={{ marginRight: 8 }} />
            <RangePicker 
              onChange={(dates) => setDateRange(dates as [moment.Moment | null, moment.Moment | null])} 
              style={{ width: '100%' }}
            />
          </Col>
          <Col span={6}>
            <Select 
              defaultValue="all" 
              style={{ width: '100%' }}
              onChange={(value) => setSelectedDepartment(value)}
            >
              <Option value="all">Todos los Departamentos</Option>
              <Option value="ventas">Ventas</Option>
              <Option value="produccion">Producción</Option>
              <Option value="finanzas">Finanzas</Option>
              <Option value="rh">Recursos Humanos</Option>
            </Select>
          </Col>
          <Col span={12} style={{ textAlign: 'right' }}>
            <Space>
              <Button>Filtrar</Button>
              <Button type="primary">Exportar Datos</Button>
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
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Clientes Nuevos"
              value={125}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Productos Activos"
              value={245}
              valueStyle={{ color: '#cf1322' }}
            />
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
          </Card>
        </Col>
      </Row>

      <Tabs 
        defaultActiveKey="dashboard" 
        onChange={setActiveTab}
        style={{ marginBottom: 24 }}
      >
        <TabPane tab={<><DashboardOutlined /> Dashboards</>} key="dashboard">
          <Row gutter={16}>
            <Col span={16}>
              <Card title="Evolución de Ventas" style={{ marginBottom: 16 }}>
                <Column {...columnConfig} height={300} />
              </Card>
              
              <Card title="Distribución de Ventas por Producto">
                <div style={{ height: 300 }}>
                  {/* Placeholder para gráfico de torta */}
                  <div style={{ 
                    height: '100%', 
                    display: 'flex', 
                    alignItems: 'center', 
                    justifyContent: 'center',
                    border: '1px solid #f0f0f0',
                    borderRadius: '4px'
                  }}>
                    <Text type="secondary">Gráfico de distribución de productos por ventas</Text>
                  </div>
                </div>
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
                        <Tag color={record.estado === 'success' ? 'green' : record.estado === 'error' ? 'red' : 'orange'}>
                          {val}
                        </Tag>
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
        
        <TabPane tab={<><LineChartOutlined /> Reportes</>} key="reports">
          <Card>
            <Table
              dataSource={reportData}
              columns={[
                { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
                { 
                  title: 'Tipo', 
                  dataIndex: 'tipo', 
                  key: 'tipo',
                  render: (tipo) => (
                    <Tag color={
                      tipo === 'ventas' ? 'blue' : 
                      tipo === 'finanzas' ? 'green' : 
                      tipo === 'producción' ? 'orange' : 'purple'
                    }>
                      {tipo.charAt(0).toUpperCase() + tipo.slice(1)}
                    </Tag>
                  )
                },
                { title: 'Autor', dataIndex: 'autor', key: 'autor' },
                { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
                {
                  title: 'Acciones',
                  key: 'acciones',
                  render: () => (
                    <Space size="middle">
                      <Button type="link" icon={<EyeOutlined />}>Ver</Button>
                      <Button type="link" icon={<EditOutlined />}>Editar</Button>
                      <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
                    </Space>
                  ),
                },
              ]}
              rowKey="id"
            />
          </Card>
        </TabPane>
        
        <TabPane tab={<><PieChartOutlined /> Análisis Predictivo</>} key="analysis">
          <Card>
            <Table
              dataSource={analysisData}
              columns={[
                { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
                { title: 'Modelo', dataIndex: 'modelo', key: 'modelo' },
                { 
                  title: 'Precisión', 
                  dataIndex: 'precision', 
                  key: 'precision',
                  render: (val) => `${val}%`
                },
                { title: 'Última Ejecución', dataIndex: 'ultima_ejecución', key: 'ultima_ejecución' },
                {
                  title: 'Acciones',
                  key: 'acciones',
                  render: () => (
                    <Space size="middle">
                      <Button type="link" icon={<EyeOutlined />}>Ver Detalles</Button>
                      <Button type="link" icon={<EditOutlined />}>Reentrenar</Button>
                    </Space>
                  ),
                },
              ]}
              rowKey="id"
            />
          </Card>
        </TabPane>
      </Tabs>
    </div>
  );
};

export default BusinessIntelligenceDashboard;