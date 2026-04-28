import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  RobotOutlined,
  PercentageOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  SyncOutlined,
  TagOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const AutoClassification: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [ruleModalVisible, setRuleModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('transactions');
  const [form] = Form.useForm();
  const [ruleForm] = Form.useForm();
  
  // Datos simulados para transacciones
  const transactionData = [
    { id: '1', fecha: '2023-04-15', descripcion: 'Pago proveedor Telmex', monto: 12500, tipo: 'egreso', cuenta_origen: 'Banco Azteca', cuenta_destino: 'Telmex', clasificacion: 'Servicios', estado: 'clasificado', confianza: 95 },
    { id: '2', fecha: '2023-04-14', descripcion: 'Venta cliente Moda S.A.', monto: 45000, tipo: 'ingreso', cuenta_origen: 'Cliente', cuenta_destino: 'Banco Azteca', clasificacion: 'Ventas', estado: 'clasificado', confianza: 98 },
    { id: '3', fecha: '2023-04-12', descripcion: 'Pago nómina', monto: 185000, tipo: 'egreso', cuenta_origen: 'Banco Azteca', cuenta_destino: 'Empleados', clasificacion: 'Nómina', estado: 'manual', confianza: 65 },
    { id: '4', fecha: '2023-04-10', descripcion: 'Compra materia prima', monto: 75000, tipo: 'egreso', cuenta_origen: 'Banco Azteca', cuenta_destino: 'Proveedor ABC', clasificacion: 'Costos', estado: 'clasificado', confianza: 92 },
  ];

  // Datos simulados para reglas de clasificación
  const ruleData = [
    { id: '1', nombre: 'Regla Nómina', patron: 'nómina|salario|sueldo', cuenta: 'Nómina', tipo: 'egreso', estado: 'activo' },
    { id: '2', nombre: 'Regla Ventas', patron: 'venta|cliente|factura', cuenta: 'Ventas', tipo: 'ingreso', estado: 'activo' },
    { id: '3', nombre: 'Regla Servicios', patron: 'telmex|cfe|agua', cuenta: 'Servicios', tipo: 'egreso', estado: 'activo' },
    { id: '4', nombre: 'Regla Costos', patron: 'materia|prima|proveed', cuenta: 'Costos', tipo: 'egreso', estado: 'inactivo' },
  ];

  const columnasTransacciones = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Monto', 
      dataIndex: 'monto', 
      key: 'monto',
      render: (monto: number) => `$${monto.toLocaleString()}`
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'ingreso') color = 'green';
        if (tipo === 'egreso') color = 'red';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { title: 'Cuenta Origen', dataIndex: 'cuenta_origen', key: 'cuenta_origen' },
    { title: 'Cuenta Destino', dataIndex: 'cuenta_destino', key: 'cuenta_destino' },
    { 
      title: 'Clasificación', 
      dataIndex: 'clasificacion', 
      key: 'clasificacion',
      render: (clasificacion: string) => (
        <Tag color="blue">{clasificacion}</Tag>
      )
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'clasificado') color = 'green';
        if (estado === 'manual') color = 'orange';
        if (estado === 'pendiente') color = 'blue';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { 
      title: 'Confianza', 
      dataIndex: 'confianza', 
      key: 'confianza',
      render: (confianza: number) => (
        <div>
          <Progress percent={confianza} size="small" />
          <Text>{confianza}%</Text>
        </div>
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

  const columnasReglas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Patrón', dataIndex: 'patron', key: 'patron' },
    { title: 'Cuenta Asignada', dataIndex: 'cuenta', key: 'cuenta' },
    { 
      title: 'Tipo Transacción', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'ingreso') color = 'green';
        if (tipo === 'egreso') color = 'red';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={estado === 'activo' ? 'green' : 'default'}>
          {estado}
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

  const handleCrearTransaccion = () => {
    setModalVisible(true);
  };

  const handleCrearRegla = () => {
    setRuleModalVisible(true);
  };

  const handleGuardarTransaccion = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear transacción:', error);
    }
  };

  const handleGuardarRegla = async () => {
    try {
      const values = await ruleForm.validateFields();
      console.log('Valores del formulario:', values);
      setRuleModalVisible(false);
      ruleForm.resetFields();
    } catch (error) {
      console.error('Error al crear regla:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><RobotOutlined /> Clasificación Automática de Transacciones</Title>
          <Text>
            IA que aprende a categorizar movimientos financieros automáticamente según reglas definidas
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'transactions' ? handleCrearTransaccion : handleCrearRegla}>
            Nuevo {activeTab === 'transactions' ? 'Movimiento' : 'Regla'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Transacciones Procesadas"
              value={1248}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Clasificadas Automáticamente"
              value={1126}
              prefix={<RobotOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Precisión Promedio"
              value={92.4}
              precision={1}
              prefix={<PercentageOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Reglas Activas"
              value={24}
              prefix={<TagOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="transactions" onChange={setActiveTab}>
        <TabPane tab="Transacciones" key="transactions">
          <Card className="dashboard-card">
            <Table 
              dataSource={transactionData} 
              columns={columnasTransacciones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Reglas de Clasificación" key="rules">
          <Card className="dashboard-card">
            <Table 
              dataSource={ruleData} 
              columns={columnasReglas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nueva Transacción"
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
          onFinish={handleGuardarTransaccion}
        >
          <Form.Item name="fecha" label="Fecha de la Transacción" rules={[{ required: true, message: 'Seleccione la fecha de la transacción' }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción" rules={[{ required: true, message: 'Ingrese la descripción de la transacción' }]}>
            <Input placeholder="Ej: Pago proveedor Telmex" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="monto" label="Monto" rules={[{ required: true, message: 'Ingrese el monto de la transacción' }]}>
                <InputNumber 
                  placeholder="Monto de la transacción"
                  style={{ width: '100%' }}
                  formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
                  parser={value => value!.replace(/\$\s?|(,*)/g, '')}
                />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Transacción" rules={[{ required: true, message: 'Seleccione el tipo de transacción' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="ingreso">Ingreso</Option>
                  <Option value="egreso">Egreso</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="cuenta_origen" label="Cuenta Origen">
                <Select placeholder="Seleccione la cuenta origen">
                  <Option value="banco_azteca">Banco Azteca</Option>
                  <Option value="banco_santander">Banco Santander</Option>
                  <Option value="caja_general">Caja General</Option>
                  <Option value="cliente">Cliente</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="cuenta_destino" label="Cuenta Destino">
                <Select placeholder="Seleccione la cuenta destino">
                  <Option value="telmex">Telmex</Option>
                  <Option value="empleados">Empleados</Option>
                  <Option value="proveedor_abc">Proveedor ABC</Option>
                  <Option value="ventas">Ventas</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="clasificacion" label="Clasificación Manual (opcional)">
            <Select placeholder="Seleccione la clasificación manual (si difiere de la automática)">
              <Option value="ventas">Ventas</Option>
              <Option value="nómina">Nómina</Option>
              <Option value="servicios">Servicios</Option>
              <Option value="costos">Costos</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="notas" label="Notas Adicionales">
            <TextArea placeholder="Notas adicionales sobre la transacción" rows={4} />
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
                Crear Transacción
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Crear Nueva Regla de Clasificación"
        open={ruleModalVisible}
        onCancel={() => {
          setRuleModalVisible(false);
          ruleForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={ruleForm}
          layout="vertical"
          onFinish={handleGuardarRegla}
        >
          <Form.Item name="nombre" label="Nombre de la Regla" rules={[{ required: true, message: 'Ingrese el nombre de la regla' }]}>
            <Input placeholder="Ej: Regla Nómina" />
          </Form.Item>
          
          <Form.Item name="patron" label="Patrón de Búsqueda" rules={[{ required: true, message: 'Ingrese el patrón de búsqueda' }]}>
            <Input placeholder="Ej: nómina|salario|sueldo (usando expresiones regulares)" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción de la regla y cuándo se aplica" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="cuenta" label="Cuenta Asignada" rules={[{ required: true, message: 'Seleccione la cuenta asignada' }]}>
                <Select placeholder="Seleccione la cuenta">
                  <Option value="ventas">Ventas</Option>
                  <Option value="nómina">Nómina</Option>
                  <Option value="servicios">Servicios</Option>
                  <Option value="costos">Costos</Option>
                  <Option value="otros">Otros</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Transacción" rules={[{ required: true, message: 'Seleccione el tipo de transacción' }]}>
                <Select placeholder="Seleccione el tipo">
                  <Option value="ingreso">Ingreso</Option>
                  <Option value="egreso">Egreso</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="estado" label="Estado" valuePropName="checked">
            <Select placeholder="Seleccione el estado">
              <Option value="activo">Activo</Option>
              <Option value="inactivo">Inactivo</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="confianza_minima" label="Confianza Mínima para Aplicar (%)">
            <InputNumber 
              placeholder="Confianza mínima para aplicar esta regla"
              min={0}
              max={100}
              defaultValue={80}
              style={{ width: '100%' }}
            />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setRuleModalVisible(false);
                ruleForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Regla
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default AutoClassification;