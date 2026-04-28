import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  ToolOutlined,
  CalendarOutlined,
  PercentageOutlined,
  ScheduleOutlined,
  FileTextOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;
const { RangePicker } = DatePicker;

const MRPManagement: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('recipes');
  const [form] = Form.useForm();
  
  // Datos simulados para recetas
  const recipeData = [
    { id: '1', nombre: 'Camisa Básica', productoFinal: 'Camisa Básica', rendimiento: 100, version: 1, activa: true },
    { id: '2', nombre: 'Pantalón Jeans', productoFinal: 'Pantalón Jeans', rendimiento: 50, version: 1, activa: true },
    { id: '3', nombre: 'Vestido Formal', productoFinal: 'Vestido Formal', rendimiento: 30, version: 2, activa: false },
  ];

  // Datos simulados para órdenes de producción
  const orderData = [
    { id: '1', codigo: 'OP-2023-001', producto: 'Camisa Básica', cantidad: 500, inicio: '2023-05-01', fin: '2023-05-10', estado: 'en_progreso', prioridad: 'media' },
    { id: '2', codigo: 'OP-2023-002', producto: 'Pantalón Jeans', cantidad: 300, inicio: '2023-05-05', fin: '2023-05-15', estado: 'programada', prioridad: 'alta' },
    { id: '3', codigo: 'OP-2023-003', producto: 'Vestido Formal', cantidad: 100, inicio: '2023-05-10', fin: '2023-05-20', estado: 'pendiente', prioridad: 'baja' },
  ];

  // Datos simulados para previsión de demanda
  const forecastData = [
    { id: '1', producto: 'Camisa Básica', periodo: 'Mayo 2023', cantidad: 800, tipo: 'venta', confianza: 90 },
    { id: '2', producto: 'Pantalón Jeans', periodo: 'Mayo 2023', cantidad: 500, tipo: 'prevision', confianza: 75 },
    { id: '3', producto: 'Vestido Formal', periodo: 'Junio 2023', cantidad: 200, tipo: 'evento', confianza: 85 },
  ];

  const columnasRecetas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Producto Final', dataIndex: 'productoFinal', key: 'productoFinal' },
    { title: 'Rendimiento', dataIndex: 'rendimiento', key: 'rendimiento' },
    { title: 'Versión', dataIndex: 'version', key: 'version' },
    { 
      title: 'Estado', 
      dataIndex: 'activa', 
      key: 'activa',
      render: (activa: boolean) => (
        <Tag color={activa ? 'green' : 'default'}>
          {activa ? 'Activa' : 'Inactiva'}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasOrdenes = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { title: 'Inicio', dataIndex: 'inicio', key: 'inicio' },
    { title: 'Fin', dataIndex: 'fin', key: 'fin' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'programada') color = 'blue';
        if (estado === 'en_progreso') color = 'gold';
        if (estado === 'completada') color = 'green';
        if (estado === 'cancelada') color = 'red';
        return <Tag color={color}>{estado.replace('_', ' ')}</Tag>;
      }
    },
    { 
      title: 'Prioridad', 
      dataIndex: 'prioridad', 
      key: 'prioridad',
      render: (prioridad: string) => {
        let color = 'default';
        if (prioridad === 'baja') color = 'green';
        if (prioridad === 'media') color = 'blue';
        if (prioridad === 'alta') color = 'orange';
        if (prioridad === 'urgente') color = 'red';
        return <Tag color={color}>{prioridad}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Cancelar</Button>
        </Space>
      ),
    },
  ];

  const columnasPrevisiones = [
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'venta') color = 'blue';
        if (tipo === 'prevision') color = 'green';
        if (tipo === 'evento') color = 'orange';
        if (tipo === 'promocion') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Confianza', 
      dataIndex: 'confianza', 
      key: 'confianza',
      render: (confianza: number) => `${confianza}%`
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearReceta = () => {
    setModalVisible(true);
  };

  const handleGuardarReceta = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear receta:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><ToolOutlined /> MRP - Planificación de Requerimientos de Materiales</Title>
          <Text>
            Sistema para calcular automáticamente las materias primas necesarias según los pedidos y pronósticos
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearReceta}>
            Nueva {activeTab === 'recipes' ? 'Receta' : 
                   activeTab === 'orders' ? 'Orden de Producción' : 
                   activeTab === 'forecasts' ? 'Previsión' : 'Receta'}
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="recipes" onChange={setActiveTab}>
        <TabPane tab="Recetas de Producción" key="recipes">
          <Card className="dashboard-card">
            <Table 
              dataSource={recipeData} 
              columns={columnasRecetas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Órdenes de Producción" key="orders">
          <Card className="dashboard-card">
            <Table 
              dataSource={orderData} 
              columns={columnasOrdenes} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Previsión de Demanda" key="forecasts">
          <Card className="dashboard-card">
            <Table 
              dataSource={forecastData} 
              columns={columnasPrevisiones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title={`Crear Nueva ${activeTab === 'recipes' ? 'Receta' : 
                 activeTab === 'orders' ? 'Orden de Producción' : 
                 activeTab === 'forecasts' ? 'Previsión de Demanda' : 'Receta'}`}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={800}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarReceta}
        >
          {activeTab === 'recipes' && (
            <>
              <Form.Item name="nombre" label="Nombre de la Receta" rules={[{ required: true, message: 'Ingrese el nombre de la receta' }]}>
                <Input placeholder="Ej: Receta para Camisa Básica" />
              </Form.Item>
              
              <Form.Item name="productoFinal" label="Producto Final" rules={[{ required: true, message: 'Seleccione el producto final' }]}>
                <Select placeholder="Seleccione el producto final">
                  <Option value="camisa-basica">Camisa Básica</Option>
                  <Option value="pantalon-jeans">Pantalón Jeans</Option>
                  <Option value="vestido-formal">Vestido Formal</Option>
                </Select>
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="rendimiento" label="Rendimiento" rules={[{ required: true, message: 'Ingrese el rendimiento' }]}>
                    <InputNumber 
                      placeholder="Cantidad producida"
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="version" label="Versión" rules={[{ required: true, message: 'Ingrese la versión' }]}>
                    <InputNumber 
                      placeholder="Versión de la receta"
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="descripcion" label="Descripción">
                <TextArea placeholder="Descripción de la receta y proceso de producción" rows={4} />
              </Form.Item>
            </>
          )}
          
          {activeTab === 'orders' && (
            <>
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="codigo" label="Código de la Orden" rules={[{ required: true, message: 'Ingrese el código de la orden' }]}>
                    <Input placeholder="Ej: OP-2023-001" />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="producto" label="Producto" rules={[{ required: true, message: 'Seleccione el producto' }]}>
                    <Select placeholder="Seleccione el producto">
                      <Option value="camisa-basica">Camisa Básica</Option>
                      <Option value="pantalon-jeans">Pantalón Jeans</Option>
                      <Option value="vestido-formal">Vestido Formal</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="cantidad" label="Cantidad Programada" rules={[{ required: true, message: 'Ingrese la cantidad' }]}>
                    <InputNumber 
                      placeholder="Cantidad a producir"
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="prioridad" label="Prioridad" rules={[{ required: true, message: 'Seleccione la prioridad' }]}>
                    <Select placeholder="Seleccione la prioridad">
                      <Option value="baja">Baja</Option>
                      <Option value="media">Media</Option>
                      <Option value="alta">Alta</Option>
                      <Option value="urgente">Urgente</Option>
                    </Select>
                  </Form.Item>
                </Col>
              </Row>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="fechaInicio" label="Fecha de Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="fechaFin" label="Fecha de Finalización">
                    <DatePicker style={{ width: '100%' }} />
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="observaciones" label="Observaciones">
                <TextArea placeholder="Observaciones sobre la orden de producción" rows={3} />
              </Form.Item>
            </>
          )}
          
          {activeTab === 'forecasts' && (
            <>
              <Form.Item name="producto" label="Producto" rules={[{ required: true, message: 'Seleccione el producto' }]}>
                <Select placeholder="Seleccione el producto">
                  <Option value="camisa-basica">Camisa Básica</Option>
                  <Option value="pantalon-jeans">Pantalón Jeans</Option>
                  <Option value="vestido-formal">Vestido Formal</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="periodo" label="Periodo" rules={[{ required: true, message: 'Seleccione el periodo' }]}>
                <RangePicker picker="month" style={{ width: '100%' }} />
              </Form.Item>
              
              <Row gutter={16}>
                <Col span={12}>
                  <Form.Item name="cantidad" label="Cantidad Prevista" rules={[{ required: true, message: 'Ingrese la cantidad prevista' }]}>
                    <InputNumber 
                      placeholder="Cantidad esperada"
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
                <Col span={12}>
                  <Form.Item name="confianza" label="Nivel de Confianza (%)" rules={[{ required: true, message: 'Ingrese el nivel de confianza' }]}>
                    <InputNumber 
                      placeholder="Nivel de confianza"
                      min={0}
                      max={100}
                      style={{ width: '100%' }}
                    />
                  </Form.Item>
                </Col>
              </Row>
              
              <Form.Item name="tipo" label="Tipo de Previsión" rules={[{ required: true, message: 'Seleccione el tipo de previsión' }]}>
                <Select placeholder="Seleccione el tipo de previsión">
                  <Option value="venta">Venta Histórica</Option>
                  <Option value="prevision">Previsión Estadística</Option>
                  <Option value="evento">Evento Especial</Option>
                  <Option value="promocion">Promoción Comercial</Option>
                  <Option value="otros">Otros</Option>
                </Select>
              </Form.Item>
              
              <Form.Item name="origen" label="Origen de la Previsión">
                <Input placeholder="Ej: Análisis de ventas, tendencias de mercado, etc." />
              </Form.Item>
            </>
          )}
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear {activeTab === 'recipes' ? 'Receta' : 
                       activeTab === 'orders' ? 'Orden' : 
                       activeTab === 'forecasts' ? 'Previsión' : 'Elemento'}
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default MRPManagement;