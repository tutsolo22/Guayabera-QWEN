import React, { useState, useEffect } from 'react';
import { Table, Button, Modal, Form as AntdForm, Input as AntdInput, Select as AntdSelect, message, Tag, Space } from 'antd';

const { Option } = AntdSelect;

const UsersList: React.FC = () => {
  const [users, setUsers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<any>(null);
  const [form] = AntdForm.useForm();

  // Mock data for users
  useEffect(() => {
    // En una implementación real, esto llamaría a la API
    setUsers([
      {
        id: '1',
        email: 'admin@empresaabc.com',
        nombre_completo: 'Juan Pérez',
        tipo_usuario: 'normal',
        tenant_id: '1',
        is_active: true
      },
      {
        id: '2',
        email: 'maria@grupotut.com',
        nombre_completo: 'María López',
        tipo_usuario: 'normal',
        tenant_id: '2',
        is_active: true
      },
      {
        id: '3',
        email: 'contacto@alexatut.com',
        nombre_completo: 'Carlos Ruiz',
        tipo_usuario: 'normal',
        tenant_id: '3',
        is_active: false
      },
      {
        id: '4',
        email: 'admin@guayabera-erp.com',
        nombre_completo: 'Super Administrador',
        tipo_usuario: 'superuser',
        tenant_id: null,
        is_active: true
      }
    ]);
  }, []);

  const showModal = (user?: any) => {
    setEditingUser(user || null);
    if (user) {
      form.setFieldsValue({
        nombre_completo: user.nombre_completo,
        email: user.email,
        tipo_usuario: user.tipo_usuario,
        is_active: String(user.is_active)
      });
    } else {
      form.resetFields();
    }
    setModalVisible(true);
  };

  const handleOk = async () => {
    try {
      const values = await form.validateFields();
      
      if (editingUser) {
        // Actualizar usuario existente
        message.success('Usuario actualizado correctamente');
        setUsers(users.map(u => u.id === editingUser.id ? {...editingUser, ...values} : u));
      } else {
        // Crear nuevo usuario
        const newUser = {
          id: String(users.length + 1),
          ...values
        };
        message.success('Usuario creado correctamente');
        setUsers([...users, newUser]);
      }
      setModalVisible(false);
      form.resetFields();
      
      // Refresh the list
      // In a real implementation, this would call the API
    } catch (error) {
      console.log('Validation failed:', error);
    }
  };

  const handleCancel = () => {
    setModalVisible(false);
    setEditingUser(null);
    form.resetFields();
  };

  const columns = [
    {
      title: 'Nombre',
      dataIndex: 'nombre_completo',
      key: 'nombre_completo',
    },
    {
      title: 'Email',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: 'Tipo de Usuario',
      dataIndex: 'tipo_usuario',
      key: 'tipo_usuario',
      render: (tipo: string) => (
        <Tag color={tipo === 'superuser' ? 'red' : 'blue'}>
          {tipo === 'superuser' ? 'Super Usuario' : 'Normal'}
        </Tag>
      ),
    },
    {
      title: 'Estado',
      dataIndex: 'is_active',
      key: 'is_active',
      render: (text: any, record: any) => (
        <Tag color={record.is_active ? 'green' : 'red'}>
          {record.is_active ? 'Activo' : 'Inactivo'}
        </Tag>
      ),
    },
    {
      title: 'Acciones',
      key: 'acciones',
      render: (record: any) => (
        <Space>
          <Button type="link" onClick={() => showModal(record)}>Editar</Button>
          <Button danger type="link">Eliminar</Button>
        </Space>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <h2 style={{ color: '#1B365D', marginBottom: 16 }}>Gestión de Usuarios</h2>
      
      <Button 
        type="primary" 
        style={{ marginBottom: 16 }}
        onClick={() => showModal()}
      >
        Agregar Usuario
      </Button>
      
      <Table 
        dataSource={users} 
        columns={columns} 
        loading={loading}
        rowKey="id"
      />
      
      <Modal
        title={editingUser ? "Editar Usuario" : "Agregar Usuario"}
        open={modalVisible}
        onOk={handleOk}
        onCancel={handleCancel}
        okText="Guardar"
        cancelText="Cancelar"
      >
        <AntdForm
          layout="vertical"
          form={form}
          name="user_form"
        >
          <AntdForm.Item
            name="nombre_completo"
            label="Nombre Completo"
            rules={[{ required: true, message: 'Por favor ingrese el nombre completo' }]}
          >
            <AntdInput id="nombre-completo-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="email"
            label="Email"
            rules={[
              { required: true, message: 'Por favor ingrese el email' },
              { type: 'email', message: 'Ingrese un email válido' }
            ]}
          >
            <AntdInput id="email-input" />
          </AntdForm.Item>
          
          <AntdForm.Item
            name="tipo_usuario"
            label="Tipo de Usuario"
            rules={[{ required: true, message: 'Por favor seleccione el tipo de usuario' }]}
          >
            <AntdSelect placeholder="Seleccione el tipo de usuario">
              <Option value="normal">Normal</Option>
              <Option value="superuser">Super Usuario</Option>
            </AntdSelect>
          </AntdForm.Item>
          
          <AntdForm.Item
            name="is_active"
            label="¿Está Activo?"
            rules={[{ required: true, message: 'Por favor seleccione el estado del usuario' }]}
          >
            <AntdSelect id="is_active" placeholder="Seleccione una opción">
              <Option value="true">Sí</Option>
              <Option value="false">No</Option>
            </AntdSelect>
          </AntdForm.Item>
        </AntdForm>
      </Modal>
    </div>
  );
};

export default UsersList;