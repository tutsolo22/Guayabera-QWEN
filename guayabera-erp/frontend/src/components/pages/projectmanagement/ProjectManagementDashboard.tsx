import React from 'react';
import { Card, Row, Col, Statistic, Button, Typography, Table, Tag, Alert } from 'antd';
import { 
  ProjectOutlined, 
  PlusOutlined, 
  UsergroupAddOutlined, 
  CalendarOutlined,
  CheckSquareOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;

const ProjectManagementDashboard: React.FC = () => {
  const projects = [
    { key: '1', id: 'PROY-001', nombre: 'Lanzamiento Colección Verano', lider: 'Ana López', estado: 'En Progreso', inicio: '2023-03-01', fin: '2023-05-30', avance: 65 },
    { key: '2', id: 'PROY-002', nombre: 'Implementación Nuevos Equipos', lider: 'Carlos Ramírez', estado: 'Planeado', inicio: '2023-04-15', fin: '2023-06-30', avance: 0 },
    { key: '3', id: 'PROY-003', nombre: 'Optimización Procesos Producción', lider: 'José Martínez', estado: 'Completado', inicio: '2023-01-15', fin: '2023-03-30', avance: 100 },
    { key: '4', id: 'PROY-004', nombre: 'Digitalización Documentos', lider: 'Luisa Gómez', estado: 'En Progreso', inicio: '2023-02-01', fin: '2023-04-20', avance: 85 },
  ];

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Líder', dataIndex: 'lider', key: 'lider' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'Completado') color = 'green';
        if (estado === 'En Progreso') color = 'blue';
        if (estado === 'Planeado') color = 'orange';
        if (estado === 'Retrasado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Inicio', dataIndex: 'inicio', key: 'inicio' },
    { title: 'Fin', dataIndex: 'fin', key: 'fin' },
    { 
      title: 'Avance', 
      dataIndex: 'avance', 
      key: 'avance',
      render: (avance: number) => (
        <div>
          <div style={{ width: '100%', backgroundColor: '#f0f0f0', borderRadius: 4 }}>
            <div 
              style={{ 
                width: `${avance}%`, 
                backgroundColor: avance >= 100 ? '#52c41a' : avance >= 75 ? '#1890ff' : '#faad14', 
                height: 16, 
                borderRadius: 4,
                textAlign: 'center',
                color: 'white',
                fontSize: 12
              }}
            >
              {avance}%
            </div>
          </div>
        </div>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <>
          <Button type="link" icon={<CheckSquareOutlined />}>Ver</Button>
          <Button type="link" icon={<UsergroupAddOutlined />}>Equipo</Button>
        </>
      ),
    },
  ];

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Módulo de Gestión de Proyectos</Title>
          <Text>
            Administración de proyectos, tareas y recursos humanos
          </Text>
        </div>
        <Button type="primary" icon={<PlusOutlined />}>
          Nuevo Proyecto
        </Button>
      </Row>
      
      <Alert
        message="Módulo en Desarrollo"
        description="Este módulo permitirá gestionar proyectos empresariales, asignar tareas y coordinar equipos de trabajo."
        type="info"
        showIcon
        style={{ marginBottom: 24 }}
      />
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Proyectos" 
              value={18} 
              prefix={<ProjectOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="En Progreso" 
              value={8} 
              prefix={<CalendarOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Completados" 
              value={6} 
              prefix={<CheckSquareOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Equipo" 
              value={42} 
              prefix={<UsergroupAddOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Table dataSource={projects} columns={columns} />
      </Card>
    </div>
  );
};

export default ProjectManagementDashboard;