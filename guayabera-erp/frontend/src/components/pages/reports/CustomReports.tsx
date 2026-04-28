import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, message } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  FileTextOutlined,
  CodeOutlined,
  PlayCircleOutlined,
  DownloadOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const CustomReports: React.FC = () => {
  const [reportModalVisible, setReportModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para reportes personalizados
  const reportData = [
    { id: '1', titulo: 'Reporte de Ventas Mensual', tipo: 'ventas', autor: 'Juan Pérez', fecha_creacion: '2023-04-15', activo: true },
    { id: '2', titulo: 'Análisis de Costos', tipo: 'finanzas', autor: 'María López', fecha_creacion: '2023-04-14', activo: true },
    { id: '3', titulo: 'Eficiencia de Producción', tipo: 'producción', autor: 'Carlos Gómez', fecha_creacion: '2023-04-13', activo: false },
    { id: '4', titulo: 'Rotación de Personal', tipo: 'RH', autor: 'Ana Martínez', fecha_creacion: '2023-04-12', activo: true },
  ];

  const columnasReportes = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Título', dataIndex: 'titulo', key: 'titulo' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'ventas') color = 'blue';
        if (tipo === 'finanzas') color = 'green';
        if (tipo === 'producción' || tipo === 'produccion') color = 'orange';
        if (tipo === 'rh') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Autor', dataIndex: 'autor', key: 'autor' },
    { title: 'Fecha de Creación', dataIndex: 'fecha_creacion', key: 'fecha_creacion' },
    { 
      title: 'Estado', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        <Tag color={activo ? 'green' : 'default'}>
          {activo ? 'Activo' : 'Inactivo'}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<PlayCircleOutlined />}>Ejecutar</Button>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
          <Button type="link" icon={<DownloadOutlined />}>Exportar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearReporte = () => {
    setReportModalVisible(true);
  };

  const handleGuardarReporte = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      message.success('Reporte personalizado creado exitosamente');
      setReportModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear reporte:', error);
      message.error('Error al crear el reporte');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><FileTextOutlined /> Reportes Personalizados</Title>
          <Text>
            Creación y gestión de reportes personalizados basados en consultas SQL
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearReporte}>
            Nuevo Reporte
          </Button>
        </Space>
      </Row>

      <Card className="dashboard-card">
        <Table 
          dataSource={reportData} 
          columns={columnasReportes} 
          pagination={{ pageSize: 10 }}
        />
      </Card>

      <Modal
        title="Crear Nuevo Reporte Personalizado"
        open={reportModalVisible}
        onCancel={() => {
          setReportModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarReporte}
        >
          <Form.Item name="titulo" label="Título del Reporte" rules={[{ required: true, message: 'Ingrese el título del reporte' }]}>
            <Input placeholder="Ej: Reporte de Ventas por Producto" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del reporte y su propósito" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Reporte" rules={[{ required: true, message: 'Seleccione el tipo de reporte' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="ventas">Ventas</Option>
                  <Option value="inventario">Inventario</Option>
                  <Option value="produccion">Producción</Option>
                  <Option value="finanzas">Finanzas</Option>
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="logistica">Logística</Option>
                  <Option value="otro">Otro</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="activo" label="Estado" rules={[{ required: true, message: 'Seleccione el estado' }]}>
                <Select placeholder="Seleccione el estado">
                  <Option value={true}>Activo</Option>
                  <Option value={false}>Inactivo</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Tabs defaultActiveKey="sql">
            <TabPane tab={<><CodeOutlined /> Consulta SQL</>} key="sql">
              <Form.Item 
                name="query_sql" 
                label="Consulta SQL" 
                rules={[{ required: true, message: 'Ingrese la consulta SQL' }]}
              >
                <TextArea 
                  placeholder={`SELECT p.nombre, SUM(v.cantidad) as total_vendido
FROM ventas_detalle v
JOIN productos p ON v.producto_id = p.id
WHERE v.fecha_venta BETWEEN :fecha_inicio AND :fecha_fin
GROUP BY p.nombre
ORDER BY total_vendido DESC`} 
                  rows={8} 
                />
              </Form.Item>
              
              <Form.Item label="Parámetros">
                <Text type="secondary">Defina los parámetros que usará en la consulta (ej: :fecha_inicio, :fecha_fin)</Text>
                <div style={{ marginTop: 8 }}>
                  <Tag color="blue">:fecha_inicio</Tag>
                  <Tag color="blue">:fecha_fin</Tag>
                  <Tag color="blue">:producto_id</Tag>
                </div>
              </Form.Item>
            </TabPane>
            
            <TabPane tab={<><FileTextOutlined /> Configuración</>} key="config">
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="intervalo_actualizacion" label="Intervalo de Actualización">
                    <Select placeholder="Seleccionar intervalo">
                      <Option value="realtime">Tiempo Real</Option>
                      <Option value="hourly">Cada Hora</Option>
                      <Option value="daily">Diario</Option>
                      <Option value="weekly">Semanal</Option>
                      <Option value="monthly">Mensual</Option>
                    </Select>
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="formato_salida" label="Formato de Salida">
                    <Select placeholder="Seleccionar formato">
                      <Option value="pdf">PDF</Option>
                      <Option value="excel">Excel</Option>
                      <Option value="csv">CSV</Option>
                      <Option value="html">HTML</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="destinatarios_correo" label="Destinatarios de Correo">
                <TextArea 
                  placeholder="Ingrese direcciones de correo electrónico separadas por coma" 
                  rows={2} 
                />
              </Form.Item>
            </TabPane>
          </Tabs>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setReportModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Reporte
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default CustomReports;