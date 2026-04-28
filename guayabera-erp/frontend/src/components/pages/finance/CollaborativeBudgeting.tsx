import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, InputNumber, Statistic } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  DollarOutlined,
  TeamOutlined,
  PercentageOutlined,
  FileTextOutlined,
  CheckCircleOutlined,
  UserOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const CollaborativeBudgeting: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [assignmentModalVisible, setAssignmentModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('budgets');
  const [form] = Form.useForm();
  const [assignmentForm] = Form.useForm();
  
  // Datos simulados para presupuestos
  const budgetData = [
    { id: '1', nombre: 'Presupuesto 2023 - Operaciones', departamento: 'Operaciones', estado: 'en_proceso', inicio: '2023-01-01', fin: '2023-12-31', total: 12500000, asignado: 8200000, porcentaje: 65.6 },
    { id: '2', nombre: 'Presupuesto 2023 - Marketing', departamento: 'Marketing', estado: 'borrador', inicio: '2023-01-01', fin: '2023-12-31', total: 5000000, asignado: 1200000, porcentaje: 24.0 },
    { id: '3', nombre: 'Presupuesto 2023 - Desarrollo', departamento: 'Desarrollo', estado: 'aprobado', inicio: '2023-01-01', fin: '2023-12-31', total: 7500000, asignado: 7500000, porcentaje: 100.0 },
    { id: '4', nombre: 'Presupuesto 2023 - RRHH', departamento: 'Recursos Humanos', estado: 'en_revision', inicio: '2023-01-01', fin: '2023-12-31', total: 4200000, asignado: 2800000, porcentaje: 66.7 },
  ];

  // Datos simulados para asignaciones
  const assignmentData = [
    { id: '1', presupuesto: 'Presupuesto 2023 - Operaciones', concepto: 'Materia Prima', responsable: 'Carlos Gómez', monto: 3500000, estado: 'aprobado', fecha_asignacion: '2023-03-15' },
    { id: '2', presupuesto: 'Presupuesto 2023 - Operaciones', concepto: 'Transporte', responsable: 'María López', monto: 1200000, estado: 'en_revision', fecha_asignacion: '2023-03-20' },
    { id: '3', presupuesto: 'Presupuesto 2023 - Marketing', concepto: 'Publicidad Digital', responsable: 'Ana Martínez', monto: 800000, estado: 'borrador', fecha_asignacion: '2023-03-10' },
    { id: '4', presupuesto: 'Presupuesto 2023 - Desarrollo', concepto: 'Software Licencias', responsable: 'Luis Fernández', monto: 2500000, estado: 'aprobado', fecha_asignacion: '2023-02-28' },
  ];

  const columnasPresupuestos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Departamento', dataIndex: 'departamento', key: 'departamento' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'borrador') color = 'orange';
        if (estado === 'en_revision') color = 'blue';
        if (estado === 'en_proceso') color = 'gold';
        if (estado === 'aprobado') color = 'green';
        if (estado === 'rechazado') color = 'red';
        return <Tag color={color}>{estado}</Tag>;
      }
    },
    { title: 'Inicio', dataIndex: 'inicio', key: 'inicio' },
    { title: 'Fin', dataIndex: 'fin', key: 'fin' },
    { 
      title: 'Total', 
      dataIndex: 'total', 
      key: 'total',
      render: (total: number) => `$${total.toLocaleString()}`
    },
    { 
      title: 'Asignado', 
      dataIndex: 'asignado', 
      key: 'asignado',
      render: (asignado: number) => `$${asignado.toLocaleString()}`
    },
    { 
      title: 'Uso', 
      dataIndex: 'porcentaje', 
      key: 'porcentaje',
      render: (porcentaje: number) => `${porcentaje}%`
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<TeamOutlined />}>Asignaciones</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasAsignaciones = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Presupuesto', dataIndex: 'presupuesto', key: 'presupuesto' },
    { title: 'Concepto', dataIndex: 'concepto', key: 'concepto' },
    { title: 'Responsable', dataIndex: 'responsable', key: 'responsable' },
    { 
      title: 'Monto', 
      dataIndex: 'monto', 
      key: 'monto',
      render: (monto: number) => `$${monto.toLocaleString()}`
    },
    { title: 'Fecha Asignación', dataIndex: 'fecha_asignacion', key: 'fecha_asignacion' },
    { 
      title: 'Estado', 
      dataIndex: 'estado', 
      key: 'estado',
      render: (estado: string) => {
        let color = 'default';
        if (estado === 'borrador') color = 'orange';
        if (estado === 'en_revision') color = 'blue';
        if (estado === 'aprobado') color = 'green';
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

  const handleCrearPresupuesto = () => {
    setModalVisible(true);
  };

  const handleCrearAsignacion = () => {
    setAssignmentModalVisible(true);
  };

  const handleGuardarPresupuesto = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear presupuesto:', error);
    }
  };

  const handleGuardarAsignacion = async () => {
    try {
      const values = await assignmentForm.validateFields();
      console.log('Valores del formulario:', values);
      setAssignmentModalVisible(false);
      assignmentForm.resetFields();
    } catch (error) {
      console.error('Error al crear asignación:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><DollarOutlined /> Presupuestación Colaborativa</Title>
          <Text>
            Participación de múltiples áreas en el proceso presupuestal con asignación de responsables
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={activeTab === 'budgets' ? handleCrearPresupuesto : handleCrearAsignacion}>
            Nuevo {activeTab === 'budgets' ? 'Presupuesto' : 'Asignación'}
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Presupuestos Activos"
              value={12}
              prefix={<FileTextOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Total Asignado"
              value={28500000}
              precision={2}
              prefix={<DollarOutlined />}
              suffix="MXN"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Uso Promedio"
              value={64.2}
              precision={1}
              prefix={<PercentageOutlined />}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Departamentos"
              value={8}
              prefix={<TeamOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="budgets" onChange={setActiveTab}>
        <TabPane tab="Presupuestos" key="budgets">
          <Card className="dashboard-card">
            <Table 
              dataSource={budgetData} 
              columns={columnasPresupuestos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Asignaciones" key="assignments">
          <Card className="dashboard-card">
            <Table 
              dataSource={assignmentData} 
              columns={columnasAsignaciones} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Presupuesto"
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
          onFinish={handleGuardarPresupuesto}
        >
          <Form.Item name="nombre" label="Nombre del Presupuesto" rules={[{ required: true, message: 'Ingrese el nombre del presupuesto' }]}>
            <Input placeholder="Ej: Presupuesto 2023 - Operaciones" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del presupuesto y objetivos" rows={4} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="departamento" label="Departamento Responsable" rules={[{ required: true, message: 'Seleccione el departamento responsable' }]}>
                <Select placeholder="Seleccione el departamento">
                  <Option value="operaciones">Operaciones</Option>
                  <Option value="marketing">Marketing</Option>
                  <Option value="desarrollo">Desarrollo</Option>
                  <Option value="rrhh">Recursos Humanos</Option>
                  <Option value="finanzas">Finanzas</Option>
                  <Option value="ventas">Ventas</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="estado" label="Estado Inicial" rules={[{ required: true, message: 'Seleccione el estado inicial' }]}>
                <Select placeholder="Seleccione el estado">
                  <Option value="borrador">Borrador</Option>
                  <Option value="en_revision">En Revisión</Option>
                  <Option value="aprobado">Aprobado</Option>
                  <Option value="rechazado">Rechazado</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="inicio" label="Fecha de Inicio" rules={[{ required: true, message: 'Seleccione la fecha de inicio' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="fin" label="Fecha de Fin" rules={[{ required: true, message: 'Seleccione la fecha de fin' }]}>
                <Input type="date" />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="total" label="Monto Total del Presupuesto" rules={[{ required: true, message: 'Ingrese el monto total' }]}>
            <InputNumber 
              placeholder="Monto total del presupuesto"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item name="colaboradores" label="Colaboradores">
            <Select 
              mode="multiple" 
              placeholder="Seleccione los colaboradores participantes"
              allowClear
            >
              <Option value="carlos_gomez">Carlos Gómez (Operaciones)</Option>
              <Option value="maria_lopez">María López (Logística)</Option>
              <Option value="ana_martinez">Ana Martínez (Marketing)</Option>
              <Option value="luis_fernandez">Luis Fernández (TI)</Option>
              <Option value="patricia_ruiz">Patricia Ruiz (Finanzas)</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="notas" label="Notas Adicionales">
            <TextArea placeholder="Notas adicionales sobre el presupuesto" rows={4} />
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
                Crear Presupuesto
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      <Modal
        title="Asignar Monto a Concepto"
        open={assignmentModalVisible}
        onCancel={() => {
          setAssignmentModalVisible(false);
          assignmentForm.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={assignmentForm}
          layout="vertical"
          onFinish={handleGuardarAsignacion}
        >
          <Form.Item name="presupuesto" label="Presupuesto Asociado" rules={[{ required: true, message: 'Seleccione el presupuesto asociado' }]}>
            <Select placeholder="Seleccione el presupuesto">
              <Option value="presupuesto_operaciones">Presupuesto 2023 - Operaciones</Option>
              <Option value="presupuesto_marketing">Presupuesto 2023 - Marketing</Option>
              <Option value="presupuesto_desarrollo">Presupuesto 2023 - Desarrollo</Option>
              <Option value="presupuesto_rrhh">Presupuesto 2023 - RRHH</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="concepto" label="Concepto" rules={[{ required: true, message: 'Ingrese el concepto' }]}>
            <Input placeholder="Ej: Materia Prima, Transporte, Publicidad, etc." />
          </Form.Item>
          
          <Form.Item name="responsable" label="Responsable de la Asignación" rules={[{ required: true, message: 'Seleccione el responsable' }]}>
            <Select placeholder="Seleccione el responsable">
              <Option value="carlos_gomez">Carlos Gómez</Option>
              <Option value="maria_lopez">María López</Option>
              <Option value="ana_martinez">Ana Martínez</Option>
              <Option value="luis_fernandez">Luis Fernández</Option>
              <Option value="patricia_ruiz">Patricia Ruiz</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="monto" label="Monto Asignado" rules={[{ required: true, message: 'Ingrese el monto asignado' }]}>
            <InputNumber 
              placeholder="Monto asignado"
              style={{ width: '100%' }}
              formatter={value => `$ ${value}`.replace(/\B(?=(\d{3})+(?!\d))/g, ',')}
              parser={value => value!.replace(/\$\s?|(,*)/g, '')}
            />
          </Form.Item>
          
          <Form.Item name="fecha_asignacion" label="Fecha de Asignación" rules={[{ required: true, message: 'Seleccione la fecha de asignación' }]}>
            <Input type="date" />
          </Form.Item>
          
          <Form.Item name="estado" label="Estado de la Asignación" rules={[{ required: true, message: 'Seleccione el estado' }]}>
            <Select placeholder="Seleccione el estado">
              <Option value="borrador">Borrador</Option>
              <Option value="en_revision">En Revisión</Option>
              <Option value="aprobado">Aprobado</Option>
              <Option value="rechazado">Rechazado</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="justificacion" label="Justificación">
            <TextArea placeholder="Justificación de la asignación de monto" rows={4} />
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setAssignmentModalVisible(false);
                assignmentForm.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Asignar Monto
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default CollaborativeBudgeting;