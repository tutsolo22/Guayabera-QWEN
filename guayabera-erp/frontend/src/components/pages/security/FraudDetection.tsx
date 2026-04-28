import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, Statistic, Progress } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  WarningOutlined,
  SecurityScanOutlined,
  FlagOutlined,
  SearchOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const FraudDetection: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [ruleModalVisible, setRuleModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('alerts');
  const [form] = Form.useForm();
  const [ruleForm] = Form.useForm();
  
  // Datos simulados para alertas de fraude
  const alertData = [
    { id: '1', fecha: '2023-04-15', tipo: 'Monto Inusual', descripcion: 'Pago de $150,000 a proveedor nuevo', prioridad: 'alta', estado: 'pendiente', confianza: 92, responsable: 'Ana Martínez' },
    { id: '2', fecha: '2023-04-14', tipo: 'Patrón Atípico', descripcion: 'Serie de compras pequeñas fuera del horario habitual', prioridad: 'media', estado: 'investigando', confianza: 78, responsable: 'Carlos Gómez' },
    { id: '3', fecha: '2023-04-12', tipo: 'Cuenta Bloqueada', descripcion: 'Intento de acceso desde ubicación desconocida', prioridad: 'baja', estado: 'cerrado', confianza: 65, responsable: 'IT Dept' },
    { id: '4', fecha: '2023-04-10', tipo: 'Doble Pago', descripcion: 'Dos pagos idénticos a mismo proveedor en corto intervalo', prioridad: 'alta', estado: 'verificado', confianza: 88, responsable: 'María López' },
  ];

  // Datos simulados para reglas de detección
  const ruleData = [
    { id: '1', nombre: 'Monto Inusual', descripcion: 'Detecta montos que exceden el 200% del promedio', activa: true, umbral: 200, severidad: 'alta' },
    { id: '2', nombre: 'Patrón Horario', descripcion: 'Detecta actividades fuera del horario laboral', activa: true, umbral: 0, severidad: 'media' },
    { id: '3', nombre: 'Cuenta Nueva', descripcion: 'Detecta pagos a cuentas nuevas sin historial', activa: true, umbral: 0, severidad: 'media' },
    { id: '4', nombre: 'Doble Pago', descripcion: 'Detecta pagos duplicados dentro de un periodo', activa: false, umbral: 48, severidad: 'baja' },
  ];

  const columnasAlertas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Fecha', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Tipo', dataIndex: 'tipo', key: 'tipo' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Prioridad', 
      dataIndex: 'prioridad', 
      key: 'prioridad',
      render: (prioridad: string) => {
        let color = 'default';
        if (prioridad === 'baja') color = 'green';
        if (prioridad === 'media') color = 'orange';
        if (prioridad === 'alta') color = 'red';
        return <Tag color={color}>{prioridad}</Tag>;
      }
    },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'pendiente') color = 'orange';
        if (estado === 'investigando') color = 'blue';
        if (estado === 'cerrado') color = 'default';
        if (estado === 'verificado') color = 'green';
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
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<SearchOutlined />}>Investigar</Button>
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<CloseCircleOutlined />} danger>Cerrar</Button>
        </Space>
      ),
    },
  ];

  const columnasReglas = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
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
      title: 'Umbral', 
      dataIndex: 'umbral', 
      key: 'umbral',
      render: (umbral: number) => `${umbral}%`
    },
    { 
      title: 'Severidad', 
      dataIndex: 'severidad', 
      key: 'severidad',
      render: (severidad: string) => {
        let color = 'default';
        if (severidad === 'baja') color = 'green';
        if (severidad === 'media') color = 'orange';
        if (severidad === 'alta') color = 'red';
        return <Tag color={color}>{severidad}</Tag>;
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

  const handleCrearAlerta = () => {
    setModalVisible(true);
  };

  const handleCrearRegla = () => {
    setRuleModalVisible(true);
  };

  const handleGuardarAlerta = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear alerta:', error);
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
          <Title level={2}><WarningOutlined /> Detección de Fraudes</Title>
          <Text>
            Identificación de patrones atípicos en transacciones y actividades sospechosas
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'alerts' ? handleCrearAlerta : handleCrearRegla}>
            Nueva {activeTab === 'alerts' ? 'Alerta' : 'Regla'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Alertas Detectadas"
              value={42}
              prefix={<FlagOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Investigando"
              value={8}
              prefix={<SearchOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Fraudes Confirmados"
              value={3}
              prefix={<WarningOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Precisión"
              value={94.2}
              precision={1}
              prefix={<CheckCircleOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="alerts" onChange={setActiveTab}>
        <TabPane tab="Alertas de Fraude" key="alerts">
          <Card className="dashboard-card">
            <Table 
              dataSource={alertData} 
              columns={columnasAlertas} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Reglas de Detección" key="rules">
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
        title="Crear Nueva Alerta de Fraude"
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
          onFinish={handleGuardarAlerta}
        >
          <Form.Item name="fecha" label="Fecha de la Alerta" rules={[{ required: true, message: 'Seleccione la fecha de la alerta' }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          
          <Form.Item name="tipo" label="Tipo de Alerta" rules={[{ required: true, message: 'Seleccione el tipo de alerta' }]}>
            <Select placeholder="Seleccione el tipo de alerta">
              <Option value="monto_inusual">Monto Inusual</Option>
              <Option value="patron_atipico">Patrón Atípico</Option>
              <Option value="cuenta_bloqueada">Cuenta Bloqueada</Option>
              <Option value="doble_pago">Doble Pago</Option>
              <Option value="acceso_no_autorizado">Acceso No Autorizado</Option>
              <Option value="otros">Otros</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción" rules={[{ required: true, message: 'Ingrese la descripción de la alerta' }]}>
            <TextArea placeholder="Descripción detallada de la alerta detectada" rows={4} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="prioridad" label="Prioridad" rules={[{ required: true, message: 'Seleccione la prioridad' }]}>
                <Select placeholder="Seleccione la prioridad">
                  <Option value="baja">Baja</Option>
                  <Option value="media">Media</Option>
                  <Option value="alta">Alta</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="confianza" label="Nivel de Confianza (%)">
                <InputNumber 
                  placeholder="Nivel de confianza en la alerta"
                  min={0}
                  max={100}
                  defaultValue={85}
                  style={{ width: '100%' }}
                />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="responsable" label="Responsable Asignado">
            <Select placeholder="Seleccione el responsable">
              <Option value="ana_martinez">Ana Martínez (Finanzas)</Option>
              <Option value="carlos_gomez">Carlos Gómez (Auditoría)</Option>
              <Option value="maria_lopez">María López (Contabilidad)</Option>
              <Option value="it_dept">Departamento de IT</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="evidencia" label="Evidencia">
            <TextArea placeholder="Descripción de la evidencia que soporta la alerta" rows={4} />
          </Form.Item>
          
          <Form.Item name="acciones_tomadas" label="Acciones Tomadas">
            <TextArea placeholder="Acciones tomadas o propuestas para investigar la alerta" rows={4} />
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
                Crear Alerta
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Crear Nueva Regla de Detección"
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
            <Input placeholder="Ej: Monto Inusual" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción" rules={[{ required: true, message: 'Ingrese la descripción de la regla' }]}>
            <TextArea placeholder="Descripción de la regla y cuándo se activa" rows={4} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="activa" label="Estado" valuePropName="checked">
                <Select placeholder="Seleccione el estado">
                  <Option value={true}>Activa</Option>
                  <Option value={false}>Inactiva</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="severidad" label="Severidad" rules={[{ required: true, message: 'Seleccione la severidad' }]}>
                <Select placeholder="Seleccione la severidad">
                  <Option value="baja">Baja</Option>
                  <Option value="media">Media</Option>
                  <Option value="alta">Alta</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="umbral" label="Umbral de Activación">
            <InputNumber 
              placeholder="Valor umbral para activar la regla"
              style={{ width: '100%' }}
            />
          </Form.Item>
          
          <Form.Item name="logica_deteccion" label="Lógica de Detección">
            <TextArea 
              placeholder="Lógica o condiciones para detectar el patrón sospechoso" 
              rows={4} 
            />
          </Form.Item>
          
          <Form.Item name="mensaje_alerta" label="Mensaje de Alerta">
            <Input.TextArea 
              placeholder="Mensaje que se mostrará cuando se active la alerta" 
              rows={2} 
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

export default FraudDetection;