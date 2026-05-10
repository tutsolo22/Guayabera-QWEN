import React, { useState, useEffect } from 'react';
import { 
  Card, 
  Table, 
  Button, 
  Form as AntdForm, 
  Input, 
  Modal, 
  Tabs, 
  message, 
  Space, 
  Popconfirm,
  Tag,
  Typography
} from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined, MailOutlined } from '@ant-design/icons';
import axios from 'axios';

const { TabPane } = Tabs;
const { Title } = Typography;

interface Tenant {
  id: string;
  name: string;
  subdomain: string;
  contact_email: string;
  descripcion: string;
  is_active: boolean;
  corporation_id?: string;
  created_at: string;
}

interface Corporation {
  id: string;
  name: string;
  descripcion: string;
  created_at: string;
}

interface License {
  id: string;
  tipo_licencia_id: string;
  codigo: string;
  fecha_inicio: string;
  fecha_fin: string;
  activa: boolean;
  tenant_id?: string;
  created_at: string;
}

const SuperAdminDashboard: React.FC = () => {
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [corporations, setCorporations] = useState<Corporation[]>([]);
  const [licenses, setLicenses] = useState<License[]>([]);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('tenants');
  
  // Forms
  const [tenantForm] = AntdForm.useForm();
  const [corporationForm] = AntdForm.useForm();
  const [licenseForm] = AntdForm.useForm();
  
  // Modals
  const [showTenantModal, setShowTenantModal] = useState(false);
  const [showCorporationModal, setShowCorporationModal] = useState(false);
  const [showInviteModal, setShowInviteModal] = useState(false);
  const [inviteForm] = AntdForm.useForm();
  const [selectedTenant, setSelectedTenant] = useState<string | null>(null);

  // Load data on mount
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [tenantsRes, corporationsRes, licensesRes] = await Promise.all([
        axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/tenants`),
        axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/corporaciones`),
        axios.get(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/licencias`)
      ]);

      setTenants(tenantsRes.data.tenants);
      setCorporations(corporationsRes.data.corporaciones);
      setLicenses(licensesRes.data.licencias);
    } catch (error) {
      message.error('Error al cargar los datos');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Tenant operations
  const handleCreateTenant = async (values: any) => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/crear-tenant`, {
        name: values.name,
        subdomain: values.subdomain,
        contact_email: values.contact_email,
        descripcion: values.descripcion
      });

      message.success('Tenant creado exitosamente');
      setShowTenantModal(false);
      tenantForm.resetFields();
      fetchData();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Error al crear el tenant');
    }
  };

  const handleActivateDeactivateTenant = async (id: string, activate: boolean) => {
    try {
      const url = activate 
        ? `${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/activar-tenant/${id}`
        : `${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/desactivar-tenant/${id}`;
        
      await axios.put(url);

      message.success(`Tenant ${activate ? 'activado' : 'desactivado'} exitosamente`);
      fetchData();
    } catch (error: any) {
      message.error(error.response?.data?.detail || `Error al ${activate ? 'activar' : 'desactivar'} el tenant`);
    }
  };

  // Corporation operations
  const handleCreateCorporation = async (values: any) => {
    try {
      await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/crear-corporacion`, {
        nombre: values.name,
        descripcion: values.descripcion
      });

      message.success('Corporación creada exitosamente');
      setShowCorporationModal(false);
      corporationForm.resetFields();
      fetchData();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Error al crear la corporación');
    }
  };

  // Invite admin operations
  const handleInviteAdmin = async (values: any) => {
    if (!selectedTenant) return;

    try {
      await axios.post(`${process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1'}/admin/invitar-tenant-admin`, {
        email: values.email,
        tenant_id: selectedTenant
      });

      message.success('Invitación enviada exitosamente');
      setShowInviteModal(false);
      inviteForm.resetFields();
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Error al enviar la invitación');
    }
  };

  // Columns for tables
  const tenantColumns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Subdominio',
      dataIndex: 'subdomain',
      key: 'subdomain',
    },
    {
      title: 'Contacto',
      dataIndex: 'contact_email',
      key: 'contact_email',
    },
    {
      title: 'Descripción',
      dataIndex: 'descripcion',
      key: 'descripcion',
    },
    {
      title: 'Estado',
      key: 'is_active',
      render: (text: any, record: Tenant) => (
        <Tag color={record.is_active ? 'success' : 'error'}>
          {record.is_active ? 'Activo' : 'Inactivo'}
        </Tag>
      ),
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (text: any, record: Tenant) => (
        <Space size="middle">
          <Button 
            icon={<MailOutlined />} 
            onClick={() => {
              setSelectedTenant(record.id);
              setShowInviteModal(true);
            }}
          >
            Invitar Admin
          </Button>
          <Popconfirm
            title={record.is_active ? "¿Desactivar este tenant?" : "¿Activar este tenant?"}
            onConfirm={() => handleActivateDeactivateTenant(record.id, !record.is_active)}
            okText="Sí"
            cancelText="No"
          >
            <Button>
              {record.is_active ? 'Desactivar' : 'Activar'}
            </Button>
          </Popconfirm>
        </Space>
      ),
    },
  ];

  const corporationColumns = [
    {
      title: 'Nombre',
      dataIndex: 'name',
      key: 'name',
    },
    {
      title: 'Descripción',
      dataIndex: 'descripcion',
      key: 'descripcion',
    },
    {
      title: 'Fecha de Creación',
      dataIndex: 'created_at',
      key: 'created_at',
    },
  ];

  const licenseColumns = [
    {
      title: 'Código',
      dataIndex: 'codigo',
      key: 'codigo',
    },
    {
      title: 'Fecha Inicio',
      dataIndex: 'fecha_inicio',
      key: 'fecha_inicio',
    },
    {
      title: 'Fecha Fin',
      dataIndex: 'fecha_fin',
      key: 'fecha_fin',
    },
    {
      title: 'Activa',
      key: 'activa',
      render: (text: any, record: License) => (
        <Tag color={record.activa ? 'success' : 'error'}>
          {record.activa ? 'Sí' : 'No'}
        </Tag>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Title level={2} style={{ color: '#1B365D', marginBottom: 24 }}>
        Panel de Administración Superior
      </Title>

      <Tabs 
        defaultActiveKey="tenants" 
        onChange={(key) => setActiveTab(key)}
        style={{ marginBottom: 24 }}
      >
        <TabPane tab="Tenants" key="tenants">
          <Card
            title="Gestión de Tenants"
            extra={
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={() => setShowTenantModal(true)}
              >
                Nuevo Tenant
              </Button>
            }
          >
            <Table 
              dataSource={tenants} 
              columns={tenantColumns} 
              rowKey="id" 
              loading={loading}
            />
          </Card>
        </TabPane>

        <TabPane tab="Corporaciones" key="corporations">
          <Card
            title="Gestión de Corporaciones"
            extra={
              <Button 
                type="primary" 
                icon={<PlusOutlined />}
                onClick={() => setShowCorporationModal(true)}
              >
                Nueva Corporación
              </Button>
            }
          >
            <Table 
              dataSource={corporations} 
              columns={corporationColumns} 
              rowKey="id" 
              loading={loading}
            />
          </Card>
        </TabPane>

        <TabPane tab="Licencias" key="licenses">
          <Card title="Gestión de Licencias">
            <Table 
              dataSource={licenses} 
              columns={licenseColumns} 
              rowKey="id" 
              loading={loading}
            />
          </Card>
        </TabPane>
      </Tabs>

      {/* Modals */}
      <Modal
        title="Crear Nuevo Tenant"
        open={showTenantModal}
        onCancel={() => {
          setShowTenantModal(false);
          tenantForm.resetFields();
        }}
        footer={null}
        destroyOnClose
      >
        <AntdForm
          form={tenantForm}
          layout="vertical"
          onFinish={handleCreateTenant}
        >
          <AntdForm.Item
            name="name"
            label="Nombre del Tenant"
            rules={[{ required: true, message: 'Por favor ingrese el nombre del tenant' }]}
          >
            <Input id="tenant-name-input" placeholder="Ej: Empresa ABC S.A." />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="subdomain"
            label="Subdominio"
            rules={[{ required: true, message: 'Por favor ingrese el subdominio' }]}
          >
            <Input id="tenant-subdomain-input" placeholder="Ej: empresaabc" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="contact_email"
            label="Correo de Contacto"
            rules={[
              { required: true, message: 'Por favor ingrese el correo de contacto' },
              { type: 'email', message: 'Ingrese un correo electrónico válido' }
            ]}
          >
            <Input id="tenant-email-input" placeholder="Ej: contacto@empresaabc.com" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="descripcion"
            label="Descripción"
          >
            <Input.TextArea id="tenant-desc-input" placeholder="Breve descripción del tenant..." />
          </AntdForm.Item>
          
          <AntdForm.Item>
            <Button type="primary" htmlType="submit" block>
              Crear Tenant
            </Button>
          </AntdForm.Item>
        </AntdForm>
      </Modal>

      <Modal
        title="Crear Nueva Corporación"
        open={showCorporationModal}
        onCancel={() => {
          setShowCorporationModal(false);
          corporationForm.resetFields();
        }}
        footer={null}
        destroyOnClose
      >
        <AntdForm
          form={corporationForm}
          layout="vertical"
          onFinish={handleCreateCorporation}
        >
          <AntdForm.Item
            name="name"
            label="Nombre de la Corporación"
            rules={[{ required: true, message: 'Por favor ingrese el nombre de la corporación' }]}
          >
            <Input id="corp-name-input" placeholder="Ej: Grupo Empresarial XYZ" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="descripcion"
            label="Descripción"
          >
            <Input.TextArea id="corp-desc-input" placeholder="Breve descripción de la corporación..." />
          </AntdForm.Item>
          
          <AntdForm.Item>
            <Button type="primary" htmlType="submit" block>
              Crear Corporación
            </Button>
          </AntdForm.Item>
        </AntdForm>
      </Modal>

      <Modal
        title="Invitar Administrador de Tenant"
        open={!!showInviteModal}
        onCancel={() => {
          setShowInviteModal(false);
          setSelectedTenant(null);
          inviteForm.resetFields();
        }}
        footer={null}
        destroyOnClose
      >
        <AntdForm
          form={inviteForm}
          layout="vertical"
          onFinish={handleInviteAdmin}
        >
          <AntdForm.Item
            name="email"
            label="Correo Electrónico del Administrador"
            rules={[
              { required: true, message: 'Por favor ingrese el correo electrónico' },
              { type: 'email', message: 'Ingrese un correo electrónico válido' }
            ]}
          >
            <Input id="admin-email-input" placeholder="Ej: admin@empresacliente.com" />
          </AntdForm.Item>
          
          <AntdForm.Item>
            <Button type="primary" htmlType="submit" block>
              Enviar Invitación
            </Button>
          </AntdForm.Item>
        </AntdForm>
      </Modal>
    </div>
  );
};

export default SuperAdminDashboard;