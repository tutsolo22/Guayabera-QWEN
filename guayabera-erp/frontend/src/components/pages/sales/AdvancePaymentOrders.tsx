import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  ShoppingCartOutlined,
  MoneyCollectOutlined,
  PercentageOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  CreditCardOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const AdvancePaymentOrders: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [paymentModalVisible, setPaymentModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('orders');
  const [form] = Form.useForm();
  const [paymentForm] = Form.useForm();
  
  // Datos simulados para pedidos con anticipo
  const orderData = [
    { id: '1', codigo: 'PED-2023-001', cliente: 'Moda S.A.', total: 45000, anticipo: 9000, saldo: 36000, porcentaje: 20, estado: 'parcial', fecha_pedido: '2023-04-10', fecha_entrega: '2023-05-15' },
    { id: '2', codigo: 'PED-2023-002', cliente: 'Tendencias SA', total: 28000, anticipo: 14000, saldo: 14000, porcentaje: 50, estado: 'parcial', fecha_pedido: '2023-04-12', fecha_entrega: '2023-05-20' },
    { id: '3', codigo: 'PED-2023-003', cliente: 'Distribuciones XYZ', total: 65000, anticipo: 0, saldo: 65000, porcentaje: 0, estado: 'sin_pago', fecha_pedido: '2023-04-15', fecha_entrega: '2023-06-01' },
    { id: '4', codigo: 'PED-2023-004', cliente: 'Ropa al Por Mayor', total: 32000, anticipo: 32000, saldo: 0, porcentaje: 100, estado: 'completo', fecha_pedido: '2023-04-05', fecha_entrega: '2023-05-10' },
  ];

  // Datos simulados para pagos
  const paymentData = [
    { id: '1', pedido: 'PED-2023-001', fecha: '2023-04-10', metodo: 'Transferencia', monto: 9000, estado: 'registrado' },
    { id: '2', pedido: 'PED-2023-002', fecha: '2023-04-12', metodo: 'Tarjeta', monto: 14000, estado: 'registrado' },
    { id: '3', pedido: 'PED-2023-004', fecha: '2023-04-05', metodo: 'Cheque', monto: 32000, estado: 'registrado' },
  ];

  const columnasPedidos = [
    { title: 'Código', dataIndex: 'codigo', key: 'codigo' },
    { title: 'Cliente', dataIndex: 'cliente', key: 'cliente' },
    { 
      title: 'Total', 
      dataIndex: 'total', 
      key: 'total',
      render: (total: number) => `$${total.toLocaleString()}`
    },
    { 
      title: 'Anticipo', 
      dataIndex: 'anticipo', 
      key: 'anticipo',
      render: (anticipo: number) => `$${anticipo.toLocaleString()}`
    },
    { 
      title: 'Saldo', 
      dataIndex: 'saldo', 
      key: 'saldo',
      render: (saldo: number) => `$${saldo.toLocaleString()}`
    },
    { 
      title: 'Anticipo %', 
      dataIndex: 'porcentaje', 
      key: 'porcentaje',
      render: (porcentaje: number) => `${porcentaje}%`
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'sin_pago') color = 'red';
        if (estado === 'parcial') color = 'orange';
        if (estado === 'completo') color = 'green';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Fecha Pedido', dataIndex: 'fecha_pedido', key: 'fecha_pedido' },
    { title: 'Fecha Entrega', dataIndex: 'fecha_entrega', key: 'fecha_entrega' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<CreditCardOutlined />} onClick={() => setPaymentModalVisible(true)}>Agregar Pago</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasPagos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Pedido', dataIndex: 'pedido', key: 'pedido' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Método', dataIndex: 'metodo', key: 'metodo' },
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
        if (estado === 'registrado') color = 'blue';
        if (estado === 'confirmado') color = 'green';
        if (estado === 'rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
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

  const handleCrearPedido = () => {
    setModalVisible(true);
  };

  const handleCrearPago = () => {
    setPaymentModalVisible(true);
  };

  const handleGuardarPedido = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear pedido:', error);
    }
  };

  const handleGuardarPago = async () => {
    try {
      const values = await paymentForm.validateFields();
      console.log('Valores del formulario:', values);
      setPaymentModalVisible(false);
      paymentForm.resetFields();
    } catch (error) {
      console.error('Error al crear pago:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><MoneyCollectOutlined /> Pedidos con Anticipo</Title>
          <Text>
            Control de cobros parciales por adelantado en pedidos especiales o personalizados
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'orders' ? handleCrearPedido : handleCrearPago}>
            Nuevo {activeTab === 'orders' ? 'Pedido' : 'Pago'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Pedidos con Anticipo"
              value={24}
              prefix={<ShoppingCartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Anticipos Recibidos"
              value={185000}
              precision={2}
              prefix={<MoneyCollectOutlined />}
              suffix="MXN"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Promedio Anticipo"
              value={36.5}
              precision={1}
              prefix={<PercentageOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Estatus Promedio"
              value={78}
              precision={0}
              prefix={<CheckCircleOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="orders" onChange={setActiveTab}>
        <TabPane tab="Pedidos con Anticipo" key="orders">
          <Card className="dashboard-card">
            <Table 
              dataSource={orderData} 
              columns={columnasPedidos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Pagos Registrados" key="payments">
          <Card className="dashboard-card">
            <Table 
              dataSource={paymentData} 
              columns={columnasPagos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Pedido con Anticipo"
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
          onFinish={handleGuardarPedido}
        >
          <Form.Item name="codigo" label="Código del Pedido" rules={[{ required: true, message: 'Ingrese el código del pedido' }]}>
            <Input placeholder="Ej: PED-2023-001" />
          </Form.Item>
          
          <Form.Item name="cliente" label="Cliente" rules={[{ required: true, message: 'Seleccione el cliente' }]}>
            <Select placeholder="Seleccione el cliente">
              <Option value="moda_sa">Moda S.A.</Option>
              <Option value="tendencias_sa">Tendencias SA</Option>
              <Option value="distribuciones_xyz">Distribuciones XYZ</Option>
              <Option value="ropa_al_por_mayor">Ropa al Por Mayor</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="producto" label="Producto/Servicio" rules={[{ required: true, message: 'Seleccione el producto/servicio' }]}>
            <Select placeholder="Seleccione el producto o servicio">
              <Option value="camisa_casual">Camisa Casual</Option>
              <Option value="pantalon_jeans">Pantalón Jeans</Option>
              <Option value="vestido_fiesta">Vestido de Fiesta</Option>
              <Option value="servicio_personalizado">Servicio de Prenda Personalizada</Option>
            </Select>
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="total" label="Total del Pedido" rules={[{ required: true, message: 'Ingrese el total del pedido' }]}>
                <InputNumber 
                  placeholder="Total del pedido"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="anticipo_req" label="Anticipo Requerido (%)" rules={[{ required: true, message: 'Ingrese el porcentaje de anticipo requerido' }]}>
                <InputNumber 
                  placeholder="Porcentaje de anticipo requerido"
                  min={0}
                  max={100}
                  style={{ width: '100%' }}
                  formatter={value => `${value}%`}
                  parser={value => value!.replace('%', '')}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="fecha_pedido" label="Fecha del Pedido" rules={[{ required: true, message: 'Seleccione la fecha del pedido' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fecha_entrega" label="Fecha de Entrega Estimada" rules={[{ required: true, message: 'Seleccione la fecha de entrega estimada' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="notas" label="Notas Adicionales">
            <TextArea placeholder="Información adicional sobre el pedido" rows={4} />
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
                Crear Pedido
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Registrar Pago de Anticipo"
        open={paymentModalVisible}
        onCancel={() => {
          setPaymentModalVisible(false);
          paymentForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={paymentForm}
          layout="vertical"
          onFinish={handleGuardarPago}
        >
          <Form.Item name="pedido" label="Pedido" rules={[{ required: true, message: 'Seleccione el pedido' }]}>
            <Select placeholder="Seleccione el pedido">
              <Option value="ped-2023-001">PED-2023-001 - Moda S.A.</Option>
              <Option value="ped-2023-002">PED-2023-002 - Tendencias SA</Option>
              <Option value="ped-2023-003">PED-2023-003 - Distribuciones XYZ</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="metodo_pago" label="Método de Pago" rules={[{ required: true, message: 'Seleccione el método de pago' }]}>
            <Select placeholder="Seleccione el método de pago">
              <Option value="transferencia">Transferencia Bancaria</Option>
              <Option value="tarjeta">Tarjeta de Débito/Crédito</Option>
              <Option value="cheque">Cheque</Option>
              <Option value="efectivo">Efectivo</Option>
              <Option value="otro">Otro</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="monto" label="Monto del Pago" rules={[{ required: true, message: 'Ingrese el monto del pago' }]}>
            <InputNumber 
              placeholder="Monto del anticipo"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item name="fecha_pago" label="Fecha del Pago" rules={[{ required: true, message: 'Seleccione la fecha del pago' }]}>
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="referencia" label="Referencia de Pago">
            <Input placeholder="Número de referencia, confirmación, etc." />
          </Form.Item>
          
          <Form.Item name="estado_pago" label="Estado del Pago" rules={[{ required: true, message: 'Seleccione el estado del pago' }]}>
            <Select placeholder="Seleccione el estado del pago">
              <Option value="registrado">Registrado</Option>
              <Option value="confirmado">Confirmado</Option>
              <Option value="rechazado">Rechazado</Option>
            </Select>
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setPaymentModalVisible(false);
                paymentForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Registrar Pago
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default AdvancePaymentOrders;