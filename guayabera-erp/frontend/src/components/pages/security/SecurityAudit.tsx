import React, { useState } from 'react';
import { Card, Row, Col, Button, Space, Typography, Table, Modal, Form, Input, Select, Tabs, Divider, Tag, DatePicker, Statistic, Badge } from 'antd';
import { 
  PlusOutlined, 
  EditOutlined, 
  DeleteOutlined,
  SafetyCertificateOutlined,
  AuditOutlined,
  LockOutlined,
  UnlockOutlined,
  UserOutlined,
  LoginOutlined,
  LogoutOutlined,
  EyeOutlined,
  EyeInvisibleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { TextArea } = Input;
const { Option } = Select;
const { TabPane } = Tabs;

const SecurityAudit: React.FC = () => {
  const [modalVisible, setModalVisible] = useState(false);
  const [activeTab, setActiveTab] = useState('logs');
  const [form] = Form.useForm();
  
  // Datos simulados para logs de auditoría
  const auditLogData = [
    { id: '1', fecha: '2023-04-15 10:30:25', usuario: 'admin', accion: 'login', recurso: 'Sistema', ip: '192.168.1.10', resultado: 'exitoso', severidad: 'baja' },
    { id: '2', fecha: '2023-04-15 10:45:12', usuario: 'carlos_gomez', accion: 'editar', recurso: 'Clientes', ip: '192.168.1.15', resultado: 'exitoso', severidad: 'media' },
    { id: '3', fecha: '2023-04-15 11:20:05', usuario: 'maria_lopez', accion: 'acceso', recurso: 'Finanzas', ip: '192.168.1.18', resultado: 'denegado', severidad: 'alta' },
    { id: '4', fecha: '2023-04-15 12:15:40', usuario: 'ana_martinez', accion: 'eliminar', recurso: 'Productos', ip: '192.168.1.20', resultado: 'exitoso', severidad: 'alta' },
  ];

  // Datos simulados para permisos
  const permissionData = [
    { id: '1', recurso: 'Clientes', rol: 'Administrador', permiso: 'lectura_escritura', estado: 'activo' },
    { id: '2', recurso: 'Finanzas', rol: 'Gerente', permiso: 'lectura', estado: 'activo' },
    { id: '3', recurso: 'Inventario', rol: 'Operador', permiso: 'lectura', estado: 'activo' },
    { id: '4', recurso: 'RRHH', rol: 'Empleado', permiso: 'ninguno', estado: 'activo' },
  ];

  const columnasLogs = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Fecha/Hora', dataIndex: 'fecha', key: 'fecha' },
    { title: 'Usuario', dataIndex: 'usuario', key: 'usuario' },
    { 
      title: 'Acción', 
      dataIndex: 'accion', 
      key: 'accion',
      render: (accion: string) => {
        let icon = null;
        switch(accion) {
          case 'login':
            icon = <LoginOutlined />;
            break;
          case 'logout':
            icon = <LogoutOutlined />;
            break;
          case 'acceso':
            icon = <EyeOutlined />;
            break;
          case 'editar':
            icon = <EditOutlined />;
            break;
          case 'eliminar':
            icon = <DeleteOutlined />;
            break;
          default:
            icon = <AuditOutlined />;
        }
        return <span>{icon} {accion}</span>;
      }
    },
    { title: 'Recurso', dataIndex: 'recurso', key: 'recurso' },
    { title: 'IP', dataIndex: 'ip', key: 'ip' },
    { 
      title: 'Resultado', 
      dataIndex: 'resultado', 
      key: 'resultado',
      render: (resultado: string) => {
        let color = 'default';
        if (resultado === 'exitoso') color = 'green';
        if (resultado === 'denegado') color = 'orange';
        if (resultado === 'fallido') color = 'red';
        return <Tag color={color}>{resultado}</Tag>;
      }
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
          <Button type="link" icon={<EyeOutlined />}>Ver Detalle</Button>
          <Button type="link" icon={<DeleteOutlined />} danger>Eliminar</Button>
        </Space>
      ),
    },
  ];

  const columnasPermisos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Recurso', dataIndex: 'recurso', key: 'recurso' },
    { title: 'Rol', dataIndex: 'rol', key: 'rol' },
    { 
      title: 'Permiso', 
      dataIndex: 'permiso', 
      key: 'permiso',
      render: (permiso: string) => {
        let color = 'default';
        if (permiso === 'lectura_escritura') color = 'green';
        if (permiso === 'lectura') color = 'blue';
        if (permiso === 'ninguno') color = 'red';
        return <Tag color={color}>{permiso.replace('_', ' ')}</Tag>;
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

  const handleCrearPermiso = () => {
    setModalVisible(true);
  };

  const handleGuardarPermiso = async () => {
    try {
      const values = await form.validateFields();
      console.log('Valores del formulario:', values);
      setModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear permiso:', error);
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}><SafetyCertificateOutlined /> Auditoría de Seguridad</Title>
          <Text>
            Registros detallados de todas las actividades y eventos de seguridad del sistema
          </Text>
        </div>
        <Space>
          <Button icon={<PlusOutlined />} onClick={handleCrearPermiso}>
            Nuevo Permiso
          </Button>
        </Space>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="Eventos Hoy"
              value={1248}
              prefix={<AuditOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Usuarios Activos"
              value={42}
              prefix={<UserOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Eventos Altas"
              value={8}
              prefix={<UnlockOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="Accesos Denegados"
              value={15}
              prefix={<LockOutlined />}
            />
          </Card>
        </Col>
      </Row>

      <Tabs defaultActiveKey="logs" onChange={setActiveTab}>
        <TabPane tab="Registros de Auditoría" key="logs">
          <Card className="dashboard-card">
            <Table 
              dataSource={auditLogData} 
              columns={columnasLogs} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
        
        <TabPane tab="Permisos de Acceso" key="permissions">
          <Card className="dashboard-card">
            <Table 
              dataSource={permissionData} 
              columns={columnasPermisos} 
              pagination={{ pageSize: 10 }}
            />
          </Card>
        </TabPane>
      </Tabs>

      <Modal
        title="Crear Nuevo Permiso de Acceso"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleGuardarPermiso}
        >
          <Form.Item name="recurso" label="Recurso" rules={[{ required: true, message: 'Seleccione el recurso' }]}>
            <Select placeholder="Seleccione el recurso">
              <Option value="clientes">Clientes</Option>
              <Option value="productos">Productos</Option>
              <Option value="ventas">Ventas</Option>
              <Option value="inventario">Inventario</Option>
              <Option value="finanzas">Finanzas</Option>
              <Option value="rrhh">Recursos Humanos</Option>
              <Option value="produccion">Producción</Option>
              <Option value="reportes">Reportes</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="rol" label="Rol" rules={[{ required: true, message: 'Seleccione el rol' }]}>
            <Select placeholder="Seleccione el rol">
              <Option value="administrador">Administrador</Option>
              <Option value="gerente">Gerente</Option>
              <Option value="supervisor">Supervisor</Option>
              <Option value="operador">Operador</Option>
              <Option value="empleado">Empleado</Option>
              <Option value="contador">Contador</Option>
              <Option value="auditor">Auditor</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="permiso" label="Tipo de Permiso" rules={[{ required: true, message: 'Seleccione el tipo de permiso' }]}>
            <Select placeholder="Seleccione el tipo de permiso">
              <Option value="lectura_escritura">Lectura y Escritura</Option>
              <Option value="lectura">Solo Lectura</Option>
              <Option value="escritura">Solo Escritura</Option>
              <Option value="ninguno">Sin Acceso</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <TextArea placeholder="Descripción del permiso y su propósito" rows={4} />
          </Form.Item>
          
          <Form.Item name="estado" label="Estado" valuePropName="checked">
            <Select placeholder="Seleccione el estado">
              <Option value="activo">Activo</Option>
              <Option value="inactivo">Inactivo</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="fecha_vigencia" label="Fecha de Vigencia">
            <DatePicker style={{ width: '100%' }} />
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
                Crear Permiso
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default SecurityAudit;