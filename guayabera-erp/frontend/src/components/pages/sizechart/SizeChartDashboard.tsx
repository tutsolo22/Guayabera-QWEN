import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  ProfileOutlined, 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  FileTextOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const SizeChartDashboard: React.FC = () => {
  const sizeCharts = [
    { key: '1', id: 'GC-001', nombre: 'Camisa Hombre Estándar', genero: 'Hombre', activo: true, creador: 'Ana López', fecha: '2023-04-01' },
    { key: '2', id: 'GC-002', nombre: 'Vestido Mujer Formal', genero: 'Mujer', activo: true, creador: 'Carlos Ramírez', fecha: '2023-04-02' },
    { key: '3', id: 'GC-003', nombre: 'Pantalón Niño Deportivo', genero: 'Niño', activo: false, creador: 'María Gómez', fecha: '2023-03-28' },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Género', 
      dataIndex: 'genero', 
      key: 'genero',
      render: (genero: string) => (
        <Tag color={genero === 'Hombre' ? 'blue' : genero === 'Mujer' ? 'pink' : 'gold'}>
          {genero}
        </Tag>
      )
    },
    { 
      title: 'Activo', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        <Tag color={activo ? 'green' : 'red'}>
          {activo ? 'Sí' : 'No'}
        </Tag>
      )
    },
    { title: 'Creador', dataIndex: 'creador', key: 'creador' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Gráficos de Tallas</Title>
          <Text>
            Gestión de tablas de tallas para diferentes tipos de prendas
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Gráfico de Talla
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar gráficos de tallas para diferentes productos textiles."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Gráficos Totales" 
              value={42} 
              prefix={<ProfileOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Activos" 
              value={38} 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Por Género" 
              value="3" 
              prefix={<ProfileOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Actualizados" 
              value="12" 
              prefix={<FileTextOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={sizeCharts} columns={columns} />
      </Card>
    </div>
  );
};

export default SizeChartDashboard;