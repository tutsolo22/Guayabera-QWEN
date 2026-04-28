import React, { useState } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, DatePicker, Tabs, Divider, message } from 'antd';
import { 
  FileTextOutlined, 
  BarChartOutlined, 
  DownloadOutlined,
  EyeOutlined,
  FilterOutlined,
  TeamOutlined,
  ToolOutlined,
  ShoppingOutlined,
  StockOutlined,
  AccountBookOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

interface Reporte {
  key: string;
  id: string;
  codigo: string;
  titulo: string;
  modulo: string;
  tipo: string;
  estado: string;
  fechaGeneracion: string;
  generadoPor: string;
}

const ReportsDashboard: React.FC = () => {
  const [filtroModalVisible, setFiltroModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para la tabla de reportes
  const reportesData: Reporte[] = [
    { key: '1', id: 'REP-001', codigo: 'RH-001', titulo: 'Reporte de Empleados Activos', modulo: 'rh', tipo: 'estadistico', estado: 'completado', fechaGeneracion: '2023-04-01', generadoPor: 'Juan Pérez' },
    { key: '2', id: 'REP-002', codigo: 'PROD-001', titulo: 'Órdenes de Producción Mensuales', modulo: 'production', tipo: 'operativo', estado: 'procesando', fechaGeneracion: '2023-04-02', generadoPor: 'María López' },
    { key: '3', id: 'REP-003', codigo: 'INV-001', titulo: 'Existencias por Almacén', modulo: 'inventory', tipo: 'control', estado: 'completado', fechaGeneracion: '2023-04-01', generadoPor: 'Carlos Ramírez' },
    { key: '4', id: 'REP-004', codigo: 'VENT-001', titulo: 'Ventas del Mes', modulo: 'sales', tipo: 'comercial', estado: 'pendiente', fechaGeneracion: '-', generadoPor: 'Ana Gómez' },
    { key: '5', id: 'REP-005', codigo: 'FIN-001', titulo: 'Balance General', modulo: 'finance', tipo: 'financiero', estado: 'completado', fechaGeneracion: '2023-03-31', generadoPor: 'Luis Fernández' },
  ];

  const columnasReportes = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Título', dataIndex: 'titulo', key: 'titulo' },
    { 
      title: 'Módulo', 
      dataIndex: 'modulo', 
      key: 'modulo',
      render: (modulo: string) => {
        let moduleName = '';
        let icon = null;
        
        switch(modulo) {
          case 'rh':
            moduleName = 'Recursos Humanos';
            icon = <TeamOutlined />;
            break;
          case 'production':
            moduleName = 'Producción';
            icon = <ToolOutlined />;
            break;
          case 'sales':
            moduleName = 'Ventas';
            icon = <ShoppingOutlined />;
            break;
          case 'inventory':
            moduleName = 'Inventario';
            icon = <StockOutlined />;
            break;
          case 'finance':
            moduleName = 'Finanzas';
            icon = <AccountBookOutlined />;
            break;
          default:
            moduleName = modulo;
        }
        
        return (
          <Space>
            {icon}
            <span>{moduleName}</span>
          </Space>
        );
      }
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'estadistico') color = 'blue';
        if (tipo === 'analitico') color = 'green';
        if (tipo === 'operativo') color = 'orange';
        if (tipo === 'financiero') color = 'purple';
        if (tipo === 'comercial') color = 'geekblue';
        if (tipo === 'control') color = 'volcano';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'procesando') color = 'blue';
        if (estado === 'completado') color = 'green';
        if (estado === 'error') color = 'red';
        if (estado === 'cancelado') color = 'gray';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Generación', dataIndex: 'fechaGeneracion', key: 'fechaGeneracion' },
    { title: 'Generado Por', dataIndex: 'generadoPor', key: 'generadoPor' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EyeOutlined />}>Ver</Button>
          <Button type="link" icon={<DownloadOutlined />}>Descargar</Button>
        </Space>
      ),
    },
  ];

  const handleAbrirFiltros = () => {
    setFiltroModalVisible(true);
  };

  const handleGenerarReporte = async () => {
    try {
      const values = await form.validateFields();
      message.success('Reporte generado exitosamente');
      setFiltroModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al generar reporte:', error);
      message.error('Error al generar el reporte');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Sistema de Reportes</Title>
          <Text>
            Generación y gestión de reportes para todos los módulos del sistema
          </Text>
        </div>
        <Space>
          <Button type="primary" icon={<FileTextOutlined />} onClick={handleAbrirFiltros}>
            Nuevo Reporte
          </Button>
        </Space>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Total Reportes" 
              value={24} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Completados" 
              value={18} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Este Mes" 
              value={12} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Pendientes" 
              value={6} 
              prefix={<BarChartOutlined />} 
              valueStyle={{ color: '#fa8c16' }} 
            />
          </Card>
        </Col>
      </Row>

      <Card className="dashboard-card">
        <Tabs 
          defaultActiveKey="1" 
          items={[
            {
              label: 'Todos los Reportes',
              key: '1',
              children: (
                <Table 
                  dataSource={reportesData} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Recursos Humanos',
              key: '2',
              children: (
                <Table 
                  dataSource={reportesData.filter(r => r.modulo === 'rh')} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Producción',
              key: '3',
              children: (
                <Table 
                  dataSource={reportesData.filter(r => r.modulo === 'production')} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Ventas',
              key: '4',
              children: (
                <Table 
                  dataSource={reportesData.filter(r => r.modulo === 'sales')} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Inventario',
              key: '5',
              children: (
                <Table 
                  dataSource={reportesData.filter(r => r.modulo === 'inventory')} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Finanzas',
              key: '6',
              children: (
                <Table 
                  dataSource={reportesData.filter(r => r.modulo === 'finance')} 
                  columns={columnasReportes} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
          ]} 
        />
      </Card>

      <Modal
        title="Generar Nuevo Reporte"
        open={filtroModalVisible}
        onCancel={() => {
          setFiltroModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGenerarReporte}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="modulo" label="Módulo" rules={[{ required: true, message: 'Seleccione un módulo' }]}>
                <Select placeholder="Seleccione el módulo">
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="production">Producción</Option>
                  <Option value="sales">Ventas</Option>
                  <Option value="inventory">Inventario</Option>
                  <Option value="finance">Finanzas</Option>
                  <Option value="crm">CRM</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Reporte" rules={[{ required: true, message: 'Seleccione un tipo' }]}>
                <Select placeholder="Seleccione el tipo de reporte">
                  <Option value="estadistico">Estadístico</Option>
                  <Option value="analitico">Analítico</Option>
                  <Option value="operativo">Operativo</Option>
                  <Option value="financiero">Financiero</Option>
                  <Option value="comercial">Comercial</Option>
                  <Option value="control">Control</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="titulo" label="Título del Reporte" rules={[{ required: true, message: 'Ingrese un título' }]}>
            <Input placeholder="Título descriptivo del reporte" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <Input.TextArea placeholder="Breve descripción del reporte" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setFiltroModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<FilterOutlined />}>
                Generar Reporte
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default ReportsDashboard;