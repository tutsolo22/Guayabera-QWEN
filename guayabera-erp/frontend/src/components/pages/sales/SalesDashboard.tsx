import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag } from 'antd';
import { PlusOutlined, ArrowUpOutlined, ArrowDownOutlined, ShoppingCartOutlined } from '@ant-design/icons';

const { Title } = Typography;

const SalesDashboard: React.FC = () => {
  // Datos simulados para la tabla de ventas
  const salesData = [
    { key: '1', id: 'VENTA-001', cliente: 'Tienda Yucateca', monto: 15000, estado: 'Completado', fecha: '2023-04-01' },
    { key: '2', id: 'VENTA-002', cliente: 'Exportadora Maya', monto: 28500, estado: 'Pendiente', fecha: '2023-04-02' },
    { key: '3', id: 'VENTA-003', cliente: 'Modas Tradicionales', monto: 9750, estado: 'Completado', fecha: '2023-04-03' },
    { key: '4', id: 'VENTA-004', cliente: 'Regalos Elegantes', monto: 12300, estado: 'Procesando', fecha: '2023-04-04' },
  ];

  const columns = [
    { title: 'ID Venta', dataIndex: 'id', key: 'id' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { 
      title: 'Monto', 
      dataIndex: 'monto', 
      key: 'monto',
      render: (monto: number) => `$${monto.toLocaleString()}` 
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Completado') color = 'green';
        if (estado === 'Pendiente') color = 'volcano';
        if (estado === 'Procesando') color = 'blue';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link">Ver</Button>
          <Button type="link">Editar</Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      <Title level={2}>Módulo de Ventas</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ventas Hoy" 
              value={12} 
              prefix={<ShoppingCartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ingresos Hoy" 
              value="$42,500" 
              precision={2}
              prefix={<ArrowUpOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ventas Mes" 
              value={342} 
              prefix={<ShoppingCartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Ingresos Mes" 
              value="$1.2M" 
              precision={2}
              prefix={<ArrowUpOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="Ventas Recientes" 
        extra={<Button type="primary" icon={<PlusOutlined />}>Nueva Venta</Button>}
        className="dashboard-card"
      >
        <Table dataSource={salesData} columns={columns} />
      </Card>
    </div>
  );
};

export default SalesDashboard;