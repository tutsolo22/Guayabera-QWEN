import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  StockOutlined,
  CarOutlined,
  EnvironmentOutlined,
  ClockCircleOutlined,
  CheckCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const TransitInventory: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [trackingModalVisible, setTrackingModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('transfers');
  const [form] = Form.useForm();
  const [trackingForm] = Form.useForm();
  
  // Datos simulados para transferencias
  const transferData = [
    { id: '1', folio: 'TR-2023-001', producto: 'Camisa Casual', cantidad: 500, origen: 'Almacén Central', destino: 'Sucursal Norte', fecha_envio: '2023-04-10', fecha_estimada: '2023-04-12', estado: 'enviado' },
    { id: '2', folio: 'TR-2023-002', producto: 'Pantalón Jeans', cantidad: 300, origen: 'Almacén Central', destino: 'Sucursal Sur', fecha_envio: '2023-04-08', fecha_estimada: '2023-04-11', estado: 'en_transito' },
    { id: '3', folio: 'TR-2023-003', producto: 'Vestido de Fiesta', cantidad: 150, origen: 'Sucursal Norte', destino: 'Almacén Central', fecha_envio: '2023-04-12', fecha_estimada: '2023-04-13', estado: 'entregado' },
    { id: '4', folio: 'TR-2023-004', producto: 'Chaqueta Formal', cantidad: 200, origen: 'Sucursal Sur', destino: 'Sucursal Norte', fecha_envio: '2023-04-15', fecha_estimada: '2023-04-17', estado: 'preparacion' },
  ];

  // Datos simulados para seguimiento
  const trackingData = [
    { id: '1', transferencia: 'TR-2023-002', ubicacion: 'Centro de Distribución', fecha: '2023-04-09', estado: 'procesado', comentario: 'Paquete recibido en centro de distribución' },
    { id: '2', transferencia: 'TR-2023-002', ubicacion: 'Camión de transporte', fecha: '2023-04-10', estado: 'transporte', comentario: 'En camino a Sucursal Sur' },
    { id: '3', transferencia: 'TR-2023-001', ubicacion: 'Sucursal Norte', fecha: '2023-04-12', estado: 'entregado', comentario: 'Entregado en Sucursal Norte' },
  ];

  const columnasTransferencias = [
    { title: 'Folio', dataIndex: 'folio', key: 'folio' },
    { title: 'Producto', dataIndex: 'producto', key: 'producto' },
    { title: 'Cantidad', dataIndex: 'cantidad', key: 'cantidad' },
    { title: 'Origen', dataIndex: 'origen', key: 'origen' },
    { title: 'Destino', dataIndex: 'destino', key: 'destino' },
    { title: 'Fecha Envío', dataIndex: 'fecha_envio', key: 'fecha_envio' },
    { title: 'Fecha Estimada', dataIndex: 'fecha_estimada', key: 'fecha_estimada' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'preparacion') color = 'orange';
        if (estado === 'enviado') color = 'blue';
        if (estado === 'en_transito') color = 'gold';
        if (estado === 'entregado') color = 'green';
        if (estado === 'retrasado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<EnvironmentOutlined />} onClick={() => setTrackingModalVisible(true)}>Seguimiento</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasSeguimiento = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Transferencia', dataIndex: 'transferencia', key: 'transferencia' },
    { title: 'Ubicación', dataIndex: 'ubicacion', key: 'ubicacion' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'procesado') color = 'blue';
        if (estado === 'transporte') color = 'gold';
        if (estado === 'entregado') color = 'green';
        if (estado === 'retrasado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Comentario', dataIndex: 'comentario', key: 'comentario' },
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

  const handleCrearTransferencia = () => {
    setModalVisible(true);
  };

  const handleCrearSeguimiento = () => {
    setTrackingModalVisible(true);
  };

  const handleGuardarTransferencia = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear transferencia:', error);
    }
  };

  const handleGuardarSeguimiento = async () => {
    try {
      const values = await trackingForm.validateFields();
      console.log('Valores del formulario:', values);
      setTrackingModalVisible(false);
      trackingForm.resetFields();
    } catch (error) {
      console.error('Error al crear seguimiento:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><CarOutlined /> Control de Inventarios en Tránsito</Title>
          <Text>
            Seguimiento de mercancías entre almacenes y puntos de venta durante su transporte
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'transfers' ? handleCrearTransferencia : handleCrearSeguimiento}>
            Nuevo {activeTab === 'transfers' ? 'Traslado' : 'Seguimiento'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Traslados Activos"
              value={12}
              prefix={<StockOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="En Tránsito"
              value={8}
              prefix={<CarOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Entregados Hoy"
              value={4}
              prefix={<CheckCircleOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Retrasados"
              value={2}
              prefix={<ClockCircleOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="transfers" onChange={setActiveTab}>
        <TabPane tab="Traslados de Inventario" key="transfers">
          <Card className="dashboard-card">
            <Table 
              dataSource={transferData} 
              columns={columnasTransferencias} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Seguimiento de Traslados" key="tracking">
          <Card className="dashboard-card">
            <Table 
              dataSource={trackingData} 
              columns={columnasSeguimiento} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Traslado de Inventario"
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
          onFinish={handleGuardarTransferencia}
        >
          <Form.Item name="folio" label="Folio del Traslado" rules={[{ required: true, message: 'Ingrese el folio del traslado' }]}>
            <Input placeholder="Ej: TR-2023-001" />
          </Form.Item>
          
          <Form.Item name="producto" label="Producto" rules={[{ required: true, message: 'Seleccione el producto' }]}>
            <Select placeholder="Seleccione el producto">
              <Option value="camisa_casual">Camisa Casual</Option>
              <Option value="pantalon_jeans">Pantalón Jeans</Option>
              <Option value="vestido_fiesta">Vestido de Fiesta</Option>
              <Option value="chaqueta_formal">Chaqueta Formal</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="cantidad" label="Cantidad" rules={[{ required: true, message: 'Ingrese la cantidad' }]}>
                <InputNumber 
                  placeholder="Cantidad a trasladar"
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="unidad_medida" label="Unidad de Medida" rules={[{ required: true, message: 'Seleccione la unidad de medida' }]}>
                <Select placeholder="Seleccione la unidad">
                  <Option value="piezas">Piezas</Option>
                  <Option value="kilogramos">Kilogramos</Option>
                  <Option value="litros">Litros</Option>
                  <Option value="metros">Metros</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="origen" label="Almacén de Origen" rules={[{ required: true, message: 'Seleccione el almacén de origen' }]}>
                <Select placeholder="Seleccione el origen">
                  <Option value="almacen_central">Almacén Central</Option>
                  <Option value="sucursal_norte">Sucursal Norte</Option>
                  <Option value="sucursal_sur">Sucursal Sur</Option>
                  <Option value="sucursal_este">Sucursal Este</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="destino" label="Almacén de Destino" rules={[{ required: true, message: 'Seleccione el almacén de destino' }]}>
                <Select placeholder="Seleccione el destino">
                  <Option value="almacen_central">Almacén Central</Option>
                  <Option value="sucursal_norte">Sucursal Norte</Option>
                  <Option value="sucursal_sur">Sucursal Sur</Option>
                  <Option value="sucursal_este">Sucursal Este</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="fecha_envio" label="Fecha de Envío" rules={[{ required: true, message: 'Seleccione la fecha de envío' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fecha_estimada" label="Fecha Estimada de Llegada" rules={[{ required: true, message: 'Seleccione la fecha estimada' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="transportista" label="Transportista">
            <Select placeholder="Seleccione el transportista">
              <Option value="propio">Flota Propia</Option>
              <Option value="externo1">Transportes Rápidos SA</Option>
              <Option value="externo2">Distribuciones Nacionales</Option>
              <Option value="externo3">Envíos Express</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="notas" label="Notas Adicionales">
            <TextArea placeholder="Información adicional sobre el traslado" rows={4} />
          </Form.Item>
          
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
                Crear Traslado
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Agregar Seguimiento a Traslado"
        open={trackingModalVisible}
        onCancel={() => {
          setTrackingModalVisible(false);
          trackingForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={trackingForm}
          layout="vertical"
          onFinish={handleGuardarSeguimiento}
        >
          <Form.Item name="transferencia" label="Traslado" rules={[{ required: true, message: 'Seleccione el traslado' }]}>
            <Select placeholder="Seleccione el traslado">
              <Option value="tr-2023-001">TR-2023-001 - Camisa Casual</Option>
              <Option value="tr-2023-002">TR-2023-002 - Pantalón Jeans</Option>
              <Option value="tr-2023-003">TR-2023-003 - Vestido de Fiesta</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="ubicacion" label="Ubicación Actual" rules={[{ required: true, message: 'Ingrese la ubicación actual' }]}>
            <Input placeholder="Ej: Centro de Distribución, Camión de Transporte, etc." />
          </Form.Item>
          
          <Form.Item name="estado" label="Estado del Seguimiento" rules={[{ required: true, message: 'Seleccione el estado' }]}>
            <Select placeholder="Seleccione el estado">
              <Option value="procesado">Procesado</Option>
              <Option value="transporte">En Transporte</Option>
              <Option value="entregado">Entregado</Option>
              <Option value="retrasado">Retrasado</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="fecha" label="Fecha del Seguimiento" rules={[{ required: true, message: 'Seleccione la fecha del seguimiento' }]}>
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="comentario" label="Comentario">
            <TextArea placeholder="Comentarios sobre el estado actual del traslado" rows={4} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setTrackingModalVisible(false);
                trackingForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Agregar Seguimiento
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default TransitInventory;