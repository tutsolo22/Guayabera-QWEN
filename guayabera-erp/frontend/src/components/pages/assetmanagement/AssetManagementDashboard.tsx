import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  ApartmentOutlined, 
  PlusOutlined, 
  BarcodeOutlined, 
  CalendarOutlined,
  ToolOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const AssetManagementDashboard: React.FC = () => {
  const assets = [
    { key: '1', id: 'ACT-001', nombre: 'Máquina de Coser Industrial', tipo: 'Maquinaria', ubicacion: 'Planta A', estado: 'Operativo', responsable: 'Carlos Ramírez', adquisicion: '2022-05-15' },
    { key: '2', id: 'ACT-002', nombre: 'Computadora Dell OptiPlex', tipo: 'Equipo de Cómputo', ubicacion: 'Oficina TI', estado: 'Mantenimiento', responsable: 'Ana López', adquisicion: '2023-01-10' },
    { key: '3', id: 'ACT-003', nombre: 'Cortadora de Telas', tipo: 'Maquinaria', ubicacion: 'Taller Corte', estado: 'Operativo', responsable: 'José Martínez', adquisicion: '2021-11-20' },
    { key: '4', id: 'ACT-004', nombre: 'Silla Ergonómica', tipo: 'Mobiliario', ubicacion: 'Oficina Gerencia', estado: 'Operativo', responsable: 'Luisa Gómez', adquisicion: '2023-02-28' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'Maquinaria') color = 'blue';
        if (tipo === 'Equipo de Cómputo') color = 'geekblue';
        if (tipo === 'Mobiliario') color = 'green';
        if (tipo === 'Vehículo') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Operativo') color = 'green';
        if (estado === 'Mantenimiento') color = 'orange';
        if (estado === 'Dañado') color = 'red';
        if (estado === 'Baja') color = 'gray';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { title: 'Adquisición', dataIndex: 'adquisicion', key: 'adquisicion' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<BarcodeOutlined />}>Ver</Button>
          <Button type="link" icon={<ToolOutlined />}>Mantenimiento</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Gestión de Activos</Title>
          <Text>
            Administración de activos fijos y equipos de la empresa
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Activo
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar los activos fijos de la empresa, su mantenimiento y depreciación."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Activos Totales" 
              value={156} 
              prefix={<ApartmentOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Operativos" 
              value={142} 
              prefix={<ApartmentOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Mantenimiento" 
              value={8} 
              prefix={<ToolOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Tipos" 
              value={5} 
              prefix={<BarcodeOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={assets} columns={columns} />
      </Card>
    </div>
  );
};

export default AssetManagementDashboard;