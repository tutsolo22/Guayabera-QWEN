import React from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag } from 'antd';
import { PlusOutlined, TruckOutlined, ShopOutlined, FileTextOutlined, UserOutlined } from '@ant-design/icons';

const { Title } = Typography;

const SupplyChainDashboard: React.FC = () => {
  // Datos simulados para la tabla de proveedores
  const suppliersData = [
    { key: '1', id: 'PROV-001', nombre: 'Proveedor Textil Sureño', contacto: 'José Martínez', telefono: '999-123-4567', estado: 'Activo' },
    { key: '2', id: 'PROV-002', nombre: 'Distribuidora Maya', contacto: 'Ana López', telefono: '999-234-5678', estado: 'Activo' },
    { key: '3', id: 'PROV-003', nombre: 'Importaciones del Norte', contacto: 'Carlos Ruiz', telefono: '999-345-6789', estado: 'Inactivo' },
    { key: '4', id: 'PROV-004', nombre: 'Comercial Textil Yucateca', contacto: 'Luisa Gómez', telefono: '999-456-7890', estado: 'Activo' },
  ];

  const purchaseOrdersData = [
    { key: '1', id: 'OC-001', proveedor: 'Proveedor Textil Sureño', monto: 45000, estado: 'Pendiente', fecha: '2023-04-01' },
    { key: '2', id: 'OC-002', proveedor: 'Distribuidora Maya', monto: 28500, estado: 'Autorizada', fecha: '2023-04-02' },
    { key: '3', id: 'OC-003', proveedor: 'Comercial Textil Yucateca', monto: 32000, estado: 'Entregada', fecha: '2023-03-28' },
  ];

  const supplierColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Contacto', dataIndex: 'contacto', key: 'contacto' },
    { title: 'Teléfono', dataIndex: 'telefono', key: 'telefono' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Activo') color = 'green';
        if (estado === 'Inactivo') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
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

  const purchaseOrderColumns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Proveedor', dataIndex: 'proveedor', key: 'proveedor' },
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
        if (estado === 'Autorizada') color = 'blue';
        if (estado === 'Pendiente') color = 'orange';
        if (estado === 'Entregada') color = 'green';
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
      <Title level={2}>Módulo de Cadena de Suministro</Title>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Proveedores" 
              value={42} 
              prefix={<ShopOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Órdenes Compra" 
              value={128} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pendientes" 
              value={15} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#ff4d4f' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Entregadas" 
              value={113} 
              prefix={<TruckOutlined />} 
              valueStyle={{ color: '#3f8600' }} 
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={12}>
          <Card 
            title="Proveedores" 
            extra={<Button type="primary" icon={<PlusOutlined />}>Nuevo Proveedor</Button>}
            className="dashboard-card"
          >
            <Table dataSource={suppliersData} columns={supplierColumns} pagination={{ pageSize: 5 }} />
          </Card>
        </Col>
        <Col span={12}>
          <Card 
            title="Órdenes de Compra Recientes" 
            extra={<Button type="primary" icon={<PlusOutlined />}>Nueva Orden</Button>}
            className="dashboard-card"
          >
            <Table dataSource={purchaseOrdersData} columns={purchaseOrderColumns} pagination={{ pageSize: 5 }} />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default SupplyChainDashboard;