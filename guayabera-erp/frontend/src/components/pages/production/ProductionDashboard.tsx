import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography } from 'antd';
import { PlusOutlined, ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';

const { Title } = Typography;

const ProductionDashboard: React.FC = () => {
  // Datos simulados para la tabla de órdenes de producción
  const ordersData = [
    { key: '1', id: 'OP-001', producto: 'Guayabera Lino Azul Marino', estado: 'En Proceso', cantidad: 150, fechaInicio: '2023-04-01', fechaFin: '2023-04-10' },
    { key: '2', id: 'OP-002', producto: 'Guayabera Algodón Rosa', estado: 'Pendiente', cantidad: 200, fechaInicio: '2023-04-05', fechaFin: '2023-04-15' },
    { key: '3', id: 'OP-003', producto: 'Guayabera Seda Blanca', estado: 'Completado', cantidad: 75, fechaInicio: '2023-03-28', fechaFin: '2023-04-02' },
  ];

  const columns = [
    { title: 'ID Orden', dataIndex: 'id', key: 'id' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Estado', dataIndex: 'estado', key: 'estado' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { title: 'Fecha Inicio', dataIndex: 'fechaInicio', key: 'fechaInicio' },
    { title: 'Fecha Fin', dataIndex: 'fechaFin', key: 'fechaFin' },
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
      <Title level={2}>Módulo de Producción</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Órdenes Activas" 
              value={12} 
              prefix={<ArrowUpOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Completadas Hoy" 
              value={5} 
              prefix={<ArrowUpOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Eficiencia" 
              value="87.5%" 
              prefix={<ArrowUpOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pendientes" 
              value={3} 
              prefix={<ArrowDownOutlined />} 
              valueStyle={{ color: '#cf1322' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card 
        title="Órdenes de Producción" 
        extra={<Button type="primary" icon={<PlusOutlined />}>Nueva Orden</Button>}
        className="dashboard-card"
      >
        <Table dataSource={ordersData} columns={columns} />
      </Card>
    </div>
  );
};

export default ProductionDashboard;