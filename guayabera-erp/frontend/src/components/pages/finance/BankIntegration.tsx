import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, message } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  BankOutlined,
  SwapOutlined,
  FileTextOutlined,
  SyncOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const BankIntegration: React.FC = () => {
  const [bankModalVisible, setBankModalVisible] = useState(false);
  const [conciliationModalVisible, setConciliationModalVisible] = useState(false);
  const [form] = Form.useForm();
  
  // Datos simulados para bancos
  const bankData = [
    { id: '1', nombre: 'Banco Nacional', numero_cuenta: '****5678', saldo: 1250000, moneda: 'MXN', estado: 'activo' },
    { id: '2', nombre: 'Banco Internacional', numero_cuenta: '****9012', saldo: 850000, moneda: 'USD', estado: 'activo' },
    { id: '3', nombre: 'Banco de Inversiones', numero_cuenta: '****3456', saldo: 2500000, moneda: 'MXN', estado: 'inactivo' },
  ];

  // Datos simulados para extractos bancarios
  const statementData = [
    { id: '1', banco: 'Banco Nacional', periodo: 'Abril 2023', fecha_inicio: '2023-04-01', fecha_fin: '2023-04-30', estado: 'procesado' },
    { id: '2', banco: 'Banco Internacional', periodo: 'Abril 2023', fecha_inicio: '2023-04-01', fecha_fin: '2023-04-30', estado: 'pendiente' },
    { id: '3', banco: 'Banco Nacional', periodo: 'Marzo 2023', fecha_inicio: '2023-03-01', fecha_fin: '2023-03-31', estado: 'conciliado' },
  ];

  const columnasBancos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Número de Cuenta', dataIndex: 'numero_cuenta', key: 'numero_cuenta' },
    { 
      title: 'Saldo', 
      dataIndex: 'saldo', 
      key: 'saldo',
      render: (saldo: number) => `$${saldo.toLocaleString()}`
    },
    { 
      title: 'Moneda', 
      dataIndex: 'moneda', 
      key: 'moneda',
      render: (moneda: string) => (
        <Tag color={moneda === 'MXN' ? 'blue' : moneda === 'USD' ? 'green' : 'orange'}>
          {moneda}
        </Tag>
      )
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
          <Button type="link" icon={<SwapOutlined />}>Conciliar</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasExtractos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Banco', dataIndex: 'banco', key: 'banco' },
    { title: 'Periodo', dataIndex: 'periodo', key: 'periodo' },
    { title: 'Fecha Inicio', dataIndex: 'fecha_inicio', key: 'fecha_inicio' },
    { title: 'Fecha Fin', dataIndex: 'fecha_fin', key: 'fecha_fin' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => (
        <Tag color={
          estado === 'conciliado' ? 'green' : 
          estado === 'procesado' ? 'blue' : 'orange'
        }>
          {estado}
        </Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<FileTextOutlined />}>Ver</Button>
          <Button type="link" icon={<SyncOutlined />}>Procesar</Button>
        </Space>
      ),
    },
  ];

  const handleCrearBanco = () => {
    setBankModalVisible(true);
  };

  const handleCrearConciliacion = () => {
    setConciliationModalVisible(true);
  };

  const handleGuardarBanco = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      message.success('Banco registrado exitosamente');
      setBankModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear banco:', error);
      message.error('Error al crear el banco');
    }
  };

  const handleGuardarConciliacion = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      message.success('Conciliación iniciada exitosamente');
      setConciliationModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al iniciar conciliación:', error);
      message.error('Error al iniciar la conciliación');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><BankOutlined /> Integración Bancaria</Title>
          <Text>
            Conectividad y conciliación automática con instituciones bancarias
          </Text>
        </div>
        <Space>
          <Button icon={<SwapOutlined />} onClick={handleCrearConciliacion}>
            Nueva Conciliación
          </Button>
          <Button icon={<PlusOutlined />} onClick={handleCrearBanco}>
            Nuevo Banco
          </Button>
        </Space>
      </Row>

      <Tabs defaultActiveKey="banks">
        <TabPane tab="Bancos" key="banks">
          <Card className="dashboard-card">
            <Table 
              dataSource={bankData} 
              columns={columnasBancos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Extractos Bancarios" key="statements">
          <Card className="dashboard-card">
            <Table 
              dataSource={statementData} 
              columns={columnasExtractos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Conciliación" key="conciliation">
          <Card title="Conciliación Bancaria" className="dashboard-card">
            <Row gutter={16} style={{ marginBottom: 24 }}>
              <Col span={12}>
                <Card title="Movimientos Bancarios" size="small">
                  <Table
                    dataSource={[
                      { id: '1', fecha: '2023-04-15', descripcion: 'Venta Cliente A', importe: 50000, tipo: 'INGRESO' },
                      { id: '2', fecha: '2023-04-14', descripcion: 'Pago Proveedor X', importe: -25000, tipo: 'EGRESO' },
                      { id: '3', fecha: '2023-04-12', descripcion: 'Intereses Bancarios', importe: 1500, tipo: 'INGRESO' },
                    ]}
                    columns={[
                      { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
                      { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
                      { 
                        title: 'Importe', 
                        dataIndex: 'importe', 
                        key: 'importe',
                        render: (importe: number) => (
                          <Text type={importe >= 0 ? 'success' : 'danger'}>
                            {importe >= 0 ? '+' : ''}{importe.toLocaleString()}
                          </Text>
                        )
                      },
                      { 
                        title: 'Tipo', 
                        dataIndex: 'tipo', 
                        key: 'tipo',
                        render: (tipo: string) => (
                          <Tag color={tipo === 'INGRESO' ? 'green' : 'red'}>
                            {tipo}
                          </Tag>
                        )
                      }
                    ]}
                    pagination={false}
                    size="small"
                  />
                </Card>
              </Col>
              <Col span={12}>
                <Card title="Movimientos Contables" size="small">
                  <Table
                    dataSource={[
                      { id: '1', fecha: '2023-04-15', descripcion: 'Venta Cliente A', importe: 50000, tipo: 'INGRESO' },
                      { id: '2', fecha: '2023-04-14', descripcion: 'Pago Proveedor X', importe: -25000, tipo: 'EGRESO' },
                      { id: '3', fecha: '2023-04-11', descripcion: 'Publicidad', importe: -8000, tipo: 'EGRESO' },
                    ]}
                    columns={[
                      { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
                      { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
                      { 
                        title: 'Importe', 
                        dataIndex: 'importe', 
                        key: 'importe',
                        render: (importe: number) => (
                          <Text type={importe >= 0 ? 'success' : 'danger'}>
                            {importe >= 0 ? '+' : ''}{importe.toLocaleString()}
                          </Text>
                        )
                      },
                      { 
                        title: 'Tipo', 
                        dataIndex: 'tipo', 
                        key: 'tipo',
                        render: (tipo: string) => (
                          <Tag color={tipo === 'INGRESO' ? 'green' : 'red'}>
                            {tipo}
                          </Tag>
                        )
                      }
                    ]}
                    pagination={false}
                    size="small"
                  />
                </Card>
              </Col>
            </Row>
            <Row justify="end">
              <Space>
                <Button>Exportar Resultados</Button>
                <Button type="primary">Iniciar Conciliación Automática</Button>
              </Space>
            </Row>
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Registrar Nuevo Banco"
        open={bankModalVisible}
        onCancel={() => {
          setBankModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarBanco}
        >
          <Form.Item name="nombre" label="Nombre del Banco" rules={[{ required: true, message: 'Ingrese el nombre del banco' }]}>
            <Input placeholder="Ej: Banco Nacional" />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="numero_cuenta" label="Número de Cuenta" rules={[{ required: true, message: 'Ingrese el número de cuenta' }]}>
                <Input placeholder="Ej: 0000 1111 2222 3333" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="moneda" label="Moneda" rules={[{ required: true, message: 'Seleccione la moneda' }]}>
                <Select placeholder="Seleccione la moneda">
                  <Option value="MXN">Peso Mexicano (MXN)</Option>
                  <Option value="USD">Dólar Estadounidense (USD)</Option>
                  <Option value="EUR">Euro (EUR)</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="clave_bancaria" label="Clave Bancaria Estandarizada (CLABE)">
            <Input placeholder="Ej: 000000000000000000" />
          </Form.Item>
          
          <Form.Item name="api_conexion" label="Detalles de Conexión API">
            <TextArea 
              placeholder="Ingrese los detalles de conexión a la API del banco (URL, credenciales, etc.)" 
              rows={4} 
            />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del banco y su propósito" rows={3} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setBankModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Registrar Banco
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Nueva Conciliación Bancaria"
        open={conciliationModalVisible}
        onCancel={() => {
          setConciliationModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarConciliacion}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="banco" label="Banco" rules={[{ required: true, message: 'Seleccione el banco' }]}>
                <Select placeholder="Seleccione el banco">
                  <Option value="banco_nacional">Banco Nacional</Option>
                  <Option value="banco_internacional">Banco Internacional</Option>
                  <Option value="banco_inversiones">Banco de Inversiones</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="periodo" label="Periodo" rules={[{ required: true, message: 'Seleccione el periodo' }]}>
                <Select placeholder="Seleccione el periodo">
                  <Option value="abril_2023">Abril 2023</Option>
                  <Option value="marzo_2023">Marzo 2023</Option>
                  <Option value="febrero_2023">Febrero 2023</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="fecha_inicio" label="Fecha de Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="fecha_fin" label="Fecha de Fin" rules={[{ required: true, message: 'Seleccione la fecha de fin' }]}>
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="archivo_extracto" label="Archivo de Extracto Bancario">
            <Input type="file" />
            <Text type="secondary" style={{ display: 'block', marginTop: 8 }}>
              Suba el archivo de extracto bancario en formato CSV, TXT o formato bancario estandarizado
            </Text>
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setConciliationModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<SwapOutlined />}>
                Iniciar Conciliación
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default BankIntegration;