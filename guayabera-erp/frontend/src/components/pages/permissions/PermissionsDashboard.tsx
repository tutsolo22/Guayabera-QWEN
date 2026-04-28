import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Statistic, Table, Button, Space, Typography, Tag, Modal, Form, Input, Select, Tabs, Divider, message, TreeSelect } from 'antd';
import { 
  UserOutlined, 
  TeamOutlined, 
  LockOutlined, 
  MailOutlined,
  EditOutlined,
  DeleteOutlined,
  PlusOutlined,
  CheckCircleOutlined,
  CloseCircleOutlined
} from '@ant-design/icons';

const { Title, Text } = Typography;
const { Option } = Select;

interface Rol {
  key: string;
  id: string;
  nombre: string;
  descripcion: string;
  tipo: string;
  activo: boolean;
}

interface Permiso {
  key: string;
  id: string;
  nombre: string;
  descripcion: string;
  modulo: string;
  tipo: string;
  activo: boolean;
}

interface Usuario {
  key: string;
  id: string;
  nombre: string;
  correo: string;
  roles: string[];
  activo: boolean;
}

const PermissionsDashboard: React.FC = () => {
  const [rolesModalVisible, setRolesModalVisible] = useState(false);
  const [permisosModalVisible, setPermisosModalVisible] = useState(false);
  const [usuariosModalVisible, setUsuariosModalVisible] = useState(false);
  const [asignarRolModalVisible, setAsignarRolModalVisible] = useState(false);
  
  const [form] = Form.useForm();
  
  // Datos simulados para roles
  const rolesData: Rol[] = [
    { key: '1', id: 'ROL-001', nombre: 'Administrador', descripcion: 'Acceso completo al sistema', tipo: 'administrador', activo: true },
    { key: '2', id: 'ROL-002', nombre: 'Gerente', descripcion: 'Acceso gerencial con permisos amplios', tipo: 'gerente', activo: true },
    { key: '3', id: 'ROL-003', nombre: 'Supervisor', descripcion: 'Acceso a supervisión de operaciones', tipo: 'supervisor', activo: true },
    { key: '4', id: 'ROL-004', nombre: 'Operador', descripcion: 'Acceso a operaciones básicas', tipo: 'operador', activo: true },
    { key: '5', id: 'ROL-005', nombre: 'Contador', descripcion: 'Acceso a módulo contable', tipo: 'contador', activo: true },
  ];

  // Datos simulados para permisos
  const permisosData: Permiso[] = [
    { key: '1', id: 'PERM-001', nombre: 'Consultar Empleados', descripcion: 'Permiso para ver información de empleados', modulo: 'rh', tipo: 'consulta', activo: true },
    { key: '2', id: 'PERM-002', nombre: 'Crear Empleados', descripcion: 'Permiso para crear nuevos empleados', modulo: 'rh', tipo: 'crear', activo: true },
    { key: '3', id: 'PERM-003', nombre: 'Editar Empleados', descripcion: 'Permiso para editar información de empleados', modulo: 'rh', tipo: 'editar', activo: true },
    { key: '4', id: 'PERM-004', nombre: 'Eliminar Empleados', descripcion: 'Permiso para eliminar empleados', modulo: 'rh', tipo: 'eliminar', activo: true },
    { key: '5', id: 'PERM-005', nombre: 'Consultar Órdenes de Producción', descripcion: 'Permiso para ver órdenes de producción', modulo: 'production', tipo: 'consulta', activo: true },
    { key: '6', id: 'PERM-006', nombre: 'Crear Órdenes de Producción', descripcion: 'Permiso para crear nuevas órdenes de producción', modulo: 'production', tipo: 'crear', activo: true },
  ];

  // Datos simulados para usuarios
  const usuariosData: Usuario[] = [
    { key: '1', id: 'USR-001', nombre: 'Juan Pérez', correo: 'juan.perez@empresa.com', roles: ['Administrador'], activo: true },
    { key: '2', id: 'USR-002', nombre: 'María López', correo: 'maria.lopez@empresa.com', roles: ['Gerente', 'Contador'], activo: true },
    { key: '3', id: 'USR-003', nombre: 'Carlos Ramírez', correo: 'carlos.ramirez@empresa.com', roles: ['Supervisor'], activo: true },
    { key: '4', id: 'USR-004', nombre: 'Ana Gómez', correo: 'ana.gomez@empresa.com', roles: ['Operador'], activo: true },
    { key: '5', id: 'USR-005', nombre: 'Luis Fernández', correo: 'luis.fernandez@empresa.com', roles: ['Contador'], activo: true },
  ];

  const columnasRoles = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'administrador') color = 'red';
        if (tipo === 'gerente') color = 'orange';
        if (tipo === 'supervisor') color = 'blue';
        if (tipo === 'operador') color = 'green';
        if (tipo === 'contador') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Activo', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        activo ? 
        <Tag icon={<CheckCircleOutlined />} color="success">Sí</Tag> : 
        <Tag icon={<CloseCircleOutlined />} color="error">No</Tag>
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

  const columnasPermisos = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { title: 'Descripción', dataIndex: 'descripcion', key: 'descripcion' },
    { 
      title: 'Módulo', 
      dataIndex: 'modulo', 
      key: 'modulo',
      render: (modulo: string) => {
        let moduleName = '';
        let color = 'default';
        
        switch(modulo) {
          case 'rh':
            moduleName = 'Recursos Humanos';
            color = 'blue';
            break;
          case 'production':
            moduleName = 'Producción';
            color = 'green';
            break;
          case 'sales':
            moduleName = 'Ventas';
            color = 'orange';
            break;
          case 'inventory':
            moduleName = 'Inventario';
            color = 'purple';
            break;
          case 'finance':
            moduleName = 'Finanzas';
            color = 'volcano';
            break;
          default:
            moduleName = modulo;
        }
        
        return <Tag color={color}>{moduleName}</Tag>;
      }
    },
    { 
      title: 'Tipo', 
      dataIndex: 'tipo', 
      key: 'tipo',
      render: (tipo: string) => {
        let color = 'default';
        if (tipo === 'consulta') color = 'blue';
        if (tipo === 'crear') color = 'green';
        if (tipo === 'editar') color = 'orange';
        if (tipo === 'eliminar') color = 'red';
        if (tipo === 'exportar') color = 'geekblue';
        if (tipo === 'importar') color = 'purple';
        return <Tag color={color}>{tipo}</Tag>;
      }
    },
    { 
      title: 'Activo', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        activo ? 
        <Tag icon={<CheckCircleOutlined />} color="success">Sí</Tag> : 
        <Tag icon={<CloseCircleOutlined />} color="error">No</Tag>
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

  const columnasUsuarios = [
    { title: 'ID', dataIndex: 'id', key: 'id' },
    { title: 'Nombre', dataIndex: 'nombre', key: 'nombre' },
    { 
      title: 'Correo Electrónico', 
      dataIndex: 'correo', 
      key: 'correo',
      render: (correo: string) => (
        <Space>
          <MailOutlined /> {correo}
        </Space>
      )
    },
    { 
      title: 'Roles', 
      dataIndex: 'roles', 
      key: 'roles',
      render: (roles: string[]) => (
        <Space wrap>
          {roles.map((rol, index) => (
            <Tag key={index} color="blue">{rol}</Tag>
          ))}
        </Space>
      )
    },
    { 
      title: 'Activo', 
      dataIndex: 'activo', 
      key: 'activo',
      render: (activo: boolean) => (
        activo ? 
        <Tag icon={<CheckCircleOutlined />} color="success">Sí</Tag> : 
        <Tag icon={<CloseCircleOutlined />} color="error">No</Tag>
      )
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: () => (
        <Space size="middle">
          <Button type="link" icon={<EditOutlined />}>Editar</Button>
          <Button type="link" icon={<LockOutlined />}>Asignar Roles</Button>
        </Space>
      ),
    },
  ];

  const handleCrearRol = async () => {
    try {
      const values = await form.validateFields();
      message.success('Rol creado exitosamente');
      setRolesModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear rol:', error);
      message.error('Error al crear el rol');
    }
  };

  const handleCrearPermiso = async () => {
    try {
      const values = await form.validateFields();
      message.success('Permiso creado exitosamente');
      setPermisosModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear permiso:', error);
      message.error('Error al crear el permiso');
    }
  };

  const handleCrearUsuario = async () => {
    try {
      const values = await form.validateFields();
      message.success('Usuario creado exitosamente');
      setUsuariosModalVisible(false);
      form.resetFields();
    } catch (error) {
      console.error('Error al crear usuario:', error);
      message.error('Error al crear el usuario');
    }
  };

  return (
    <div>
      <Row justify="space-between" style={{ marginBottom: 24 }}>
        <div>
          <Title level={2}>Gestión de Permisos</Title>
          <Text>
            Administración de roles, permisos y asignación a usuarios
          </Text>
        </div>
        <Space>
          <Button type="primary" icon={<TeamOutlined />} onClick={() => setRolesModalVisible(true)}>
            Nuevo Rol
          </Button>
          <Button type="primary" icon={<LockOutlined />} onClick={() => setPermisosModalVisible(true)}>
            Nuevo Permiso
          </Button>
          <Button type="primary" icon={<UserOutlined />} onClick={() => setUsuariosModalVisible(true)}>
            Nuevo Usuario
          </Button>
        </Space>
      </Row>
      
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Roles" 
              value={5} 
              prefix={<TeamOutlined />} 
              valueStyle={{ color: '#1890ff' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Permisos" 
              value={24} 
              prefix={<LockOutlined />} 
              valueStyle={{ color: '#52c41a' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Usuarios" 
              value={42} 
              prefix={<UserOutlined />} 
              valueStyle={{ color: '#722ed1' }} 
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="stat-card">
            <Statistic 
              title="Notificaciones" 
              value={18} 
              prefix={<MailOutlined />} 
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
              label: 'Roles',
              key: '1',
              children: (
                <Table 
                  dataSource={rolesData} 
                  columns={columnasRoles} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Permisos',
              key: '2',
              children: (
                <Table 
                  dataSource={permisosData} 
                  columns={columnasPermisos} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
            {
              label: 'Usuarios',
              key: '3',
              children: (
                <Table 
                  dataSource={usuariosData} 
                  columns={columnasUsuarios} 
                  pagination={{ pageSize: 10 }}
                />
              ),
            },
          ]} 
        />
      </Card>

      {/* Modal para crear/editar roles */}
      <Modal
        title="Crear Nuevo Rol"
        open={rolesModalVisible}
        onCancel={() => {
          setRolesModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCrearRol}
        >
          <Form.Item name="nombre" label="Nombre del Rol" rules={[{ required: true, message: 'Ingrese el nombre del rol' }]}>
            <Input placeholder="Ej: Supervisor de Producción" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <Input.TextArea placeholder="Descripción del rol y sus funciones" rows={3} />
          </Form.Item>
          
          <Form.Item name="tipo" label="Tipo de Rol" rules={[{ required: true, message: 'Seleccione el tipo de rol' }]}>
            <Select placeholder="Seleccione el tipo de rol">
              <Option value="administrador">Administrador</Option>
              <Option value="gerente">Gerente</Option>
              <Option value="supervisor">Supervisor</Option>
              <Option value="operador">Operador</Option>
              <Option value="contador">Contador</Option>
              <Option value="recursos_humanos">Recursos Humanos</Option>
              <Option value="ventas">Ventas</Option>
              <Option value="produccion">Producción</Option>
              <Option value="inventario">Inventario</Option>
            </Select>
          </Form.Item>
          
          <Form.Item name="activo" label="Activo" valuePropName="checked" initialValue={true}>
            <Select>
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
            </Select>
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setRolesModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Rol
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>

      {/* Modal para crear/editar permisos */}
      <Modal
        title="Crear Nuevo Permiso"
        open={permisosModalVisible}
        onCancel={() => {
          setPermisosModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCrearPermiso}
        >
          <Form.Item name="nombre" label="Nombre del Permiso" rules={[{ required: true, message: 'Ingrese el nombre del permiso' }]}>
            <Input placeholder="Ej: Consultar Empleados" />
          </Form.Item>
          
          <Form.Item name="descripcion" label="Descripción">
            <Input.TextArea placeholder="Descripción del permiso" rows={3} />
          </Form.Item>
          
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="modulo" label="Módulo" rules={[{ required: true, message: 'Seleccione el módulo' }]}>
                <Select placeholder="Seleccione el módulo">
                  <Option value="rh">Recursos Humanos</Option>
                  <Option value="production">Producción</Option>
                  <Option value="sales">Ventas</Option>
                  <Option value="inventory">Inventario</Option>
                  <Option value="finance">Finanzas</Option>
                  <Option value="supply_chain">Cadena de Suministro</Option>
                  <Option value="purchases">Compras</Option>
                  <Option value="invoice">Facturación</Option>
                  <Option value="payroll">Nómina</Option>
                  <Option value="agents">Agentes Locales</Option>
                  <Option value="reports">Reportes</Option>
                </Select>
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="tipo" label="Tipo de Permiso" rules={[{ required: true, message: 'Seleccione el tipo de permiso' }]}>
                <Select placeholder="Seleccione el tipo de permiso">
                  <Option value="consulta">Consulta</Option>
                  <Option value="crear">Crear</Option>
                  <Option value="editar">Editar</Option>
                  <Option value="eliminar">Eliminar</Option>
                  <Option value="exportar">Exportar</Option>
                  <Option value="importar">Importar</Option>
                </Select>
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="activo" label="Activo" valuePropName="checked" initialValue={true}>
            <Select>
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
            </Select>
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setPermisosModalVisible(false);
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

      {/* Modal para crear/editar usuarios */}
      <Modal
        title="Crear Nuevo Usuario"
        open={usuariosModalVisible}
        onCancel={() => {
          setUsuariosModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={600}
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleCrearUsuario}
        >
          <Row gutter={16}>
            <Col span={12}>
              <Form.Item name="nombre" label="Nombre Completo" rules={[{ required: true, message: 'Ingrese el nombre del usuario' }]}>
                <Input placeholder="Ej: Juan Pérez García" />
              </Form.Item>
            </Col>
            <Col span={12}>
              <Form.Item name="correo" label="Correo Electrónico" rules={[
                { required: true, message: 'Ingrese el correo electrónico' },
                { type: 'email', message: 'Ingrese un correo electrónico válido' }
              ]}>
                <Input placeholder="ejemplo@empresa.com" prefix={<MailOutlined />} />
              </Form.Item>
            </Col>
          </Row>
          
          <Form.Item name="roles" label="Roles Asignados">
            <Select 
              mode="multiple" 
              placeholder="Seleccione uno o más roles"
              options={rolesData.map(rol => ({
                label: rol.nombre,
                value: rol.id
              }))}
            />
          </Form.Item>
          
          <Form.Item name="activo" label="Activo" valuePropName="checked" initialValue={true}>
            <Select>
              <Option value={true}>Sí</Option>
              <Option value={false}>No</Option>
            </Select>
          </Form.Item>
          
          <Divider />
          
          <Row justify="end">
            <Space>
              <Button onClick={() => {
                setUsuariosModalVisible(false);
                form.resetFields();
              }}>
                Cancelar
              </Button>
              <Button type="primary" htmlType="submit" icon={<PlusOutlined />}>
                Crear Usuario
              </Button>
            </Space>
          </Row>
        </Form>
      </Modal>
    </div>
  );
};

export default PermissionsDashboard;